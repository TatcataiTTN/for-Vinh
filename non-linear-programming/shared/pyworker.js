/* pyworker.js — chạy Python (Pyodide/WebAssembly) trong Web Worker: không treo trang, có thể hủy khi quá thời gian.
   Giao thức: main -> worker  {id, code, fn, tests, packages}
              worker -> main  {id, type:'status', text} | {id, type:'done', results:[{ok, got, error}]} | {id, type:'fatal', error} */
const PYODIDE_VERSION = '0.27.7';
importScripts('https://cdn.jsdelivr.net/pyodide/v' + PYODIDE_VERSION + '/full/pyodide.js');
let pyReady = null;
const loaded = new Set();

const HARNESS = `
import json, copy, math, traceback
import numpy as _np

def _norm(v):
    if isinstance(v, _np.ndarray): return [_norm(a) for a in v.tolist()]
    if isinstance(v, (_np.floating,)): return float(v)
    if isinstance(v, (_np.integer,)): return int(v)
    if isinstance(v, (_np.bool_,)): return bool(v)
    if isinstance(v, (list, tuple)): return [_norm(a) for a in v]
    if isinstance(v, dict): return {str(k): _norm(a) for k, a in v.items()}
    return v

def _eq(a, e, tol=1e-6):
    if e is None or a is None: return a is None and e is None
    if isinstance(e, bool) or isinstance(a, bool): return isinstance(a, bool) and isinstance(e, bool) and a == e
    if isinstance(e, str): return isinstance(a, str) and a == e
    if isinstance(e, (int, float)) and isinstance(a, (int, float)):
        return abs(a - e) <= tol * (1 + abs(e))
    if isinstance(e, list): return isinstance(a, list) and len(a) == len(e) and all(_eq(x, y, tol) for x, y in zip(a, e))
    if isinstance(e, dict): return isinstance(a, dict) and all(k in a and _eq(a[k], e[k], tol) for k in e)
    return a == e

def _run(code, fn, tests_json):
    tests = json.loads(tests_json)
    out = []
    ns = {}
    try:
        exec(compile(code, '<bai-lam>', 'exec'), ns)
    except Exception:
        err = traceback.format_exc(limit=1).strip().splitlines()[-1]
        return json.dumps([{'ok': False, 'got': None, 'error': 'Lỗi khi nạp mã: ' + err} for _ in tests])
    if fn not in ns or not callable(ns[fn]):
        return json.dumps([{'ok': False, 'got': None, 'error': 'Chưa định nghĩa hàm ' + fn + '(...)'} for _ in tests])
    for t in tests:
        try:
            got = _norm(ns[fn](*copy.deepcopy(t['args'])))
            try:
                ok = bool(_eq(got, t['expected']))
            except Exception:
                ok = False
            s = json.dumps(got)
            out.append({'ok': ok, 'got': s if len(s) < 400 else s[:400] + '…', 'error': None})
        except Exception:
            out.append({'ok': False, 'got': None, 'error': traceback.format_exc(limit=2).strip().splitlines()[-1]})
    return json.dumps(out)
`;

async function ensure(packages, id) {
  if (!pyReady) {
    self.postMessage({id, type: 'status', text: 'Đang tải Python (Pyodide ' + PYODIDE_VERSION + ')… lần đầu có thể mất 10–40 giây'});
    pyReady = loadPyodide();
  }
  const py = await pyReady;
  const need = packages.filter(p => !loaded.has(p));
  if (need.length) {
    self.postMessage({id, type: 'status', text: 'Đang tải thư viện: ' + need.join(', ')});
    await py.loadPackage(need);
    need.forEach(p => loaded.add(p));
    py.runPython(HARNESS);
  } else if (!loaded.has('__harness__')) {
    py.runPython(HARNESS);
  }
  loaded.add('__harness__');
  return py;
}

self.onmessage = async (ev) => {
  const {id, code, fn, tests, packages} = ev.data;
  try {
    const py = await ensure(['numpy'].concat(packages || []), id);
    self.postMessage({id, type: 'running', text: 'Đang chạy test…'});
    py.globals.set('_code', code); py.globals.set('_fn', fn); py.globals.set('_tests', JSON.stringify(tests));
    const res = py.runPython('_run(_code, _fn, _tests)');
    self.postMessage({id, type: 'done', results: JSON.parse(res)});
  } catch (e) {
    self.postMessage({id, type: 'fatal', error: String(e && e.message || e)});
  }
};
