# sage_worker_verbose.py
# Run with: sage -python sage_worker_verbose.py
import sys, json, traceback, os, time
from pathlib import Path
from sage.all import EllipticCurve

LOGDIR = Path("sage_logs")
LOGDIR.mkdir(exist_ok=True)

def write_log(label, msg, flush=True):
    p = LOGDIR / f"sage_{label}.log"
    with open(p, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        if flush:
            f.flush()

def process_task(task):
    label = task.get("label", "unknown")
    a = task.get("a_list")
    two_limit = int(task.get("two_limit", 13))
    out = {"label": label, "a_list": a, "two_limit": two_limit}
    write_log(label, f"START task: a={a} two_limit={two_limit}")
    try:
        E = EllipticCurve(a)
        write_log(label, "EllipticCurve constructed")
    except Exception as e:
        write_log(label, f"elliptic_curve_init_error: {e}")
        out["error"] = f"elliptic_curve_init_error: {e}"
        return out

    # Attempt to compute discriminant and j-invariant (helpful fallback)
    try:
        disc = E.discriminant()
        j = E.j_invariant()
        out["discriminant"] = str(disc)
        out["j_invariant"] = str(j)
        write_log(label, f"discriminant={disc} j_invariant={j}")
    except Exception as e:
        write_log(label, f"disc/j compute error: {e}")

    # two_descent (verbose)
    try:
        write_log(label, "Starting two_descent(...)")
        td = E.two_descent(second_limit=two_limit)
        out["two_descent_ok"] = True
        out["two_descent"] = str(td)
        write_log(label, "two_descent finished")
    except Exception as e:
        out["two_descent_ok"] = False
        out["two_descent_error"] = str(e)
        write_log(label, f"two_descent error: {e}")
        write_log(label, traceback.format_exc())

    # rank primary
    try:
        write_log(label, "Computing rank() (primary)")
        r = E.rank()
        out["rank_primary"] = int(r)
        write_log(label, f"rank_primary={r}")
    except Exception as e:
        out["rank_primary"] = None
        out["rank_primary_error"] = str(e)
        write_log(label, f"rank_primary_error: {e}")

    # rank fallback
    try:
        write_log(label, "Computing rank(only_use_mwrank=False) (fallback)")
        r2 = E.rank(only_use_mwrank=False)
        out["rank_fallback"] = int(r2)
        write_log(label, f"rank_fallback={r2}")
    except Exception as e:
        out["rank_fallback"] = None
        out["rank_fallback_error"] = str(e)
        write_log(label, f"rank_fallback_error: {e}")

    # optional: regulator, tamagawa, torsion, real_period if available
    try:
        write_log(label, "Attempting regulator/tamagawa/torsion/real_period (best-effort)")
        try:
            out["regulator"] = float(E.regulator()) if E.regulator() is not None else None
            write_log(label, f"regulator={out['regulator']}")
        except Exception as e:
            write_log(label, f"regulator error: {e}")
        try:
            out["tamagawa"] = str(E.tamagawa_number())
            write_log(label, f"tamagawa={out['tamagawa']}")
        except Exception as e:
            write_log(label, f"tamagawa error: {e}")
        try:
            out["torsion"] = str(E.torsion_subgroup())
            write_log(label, f"torsion={out['torsion']}")
        except Exception as e:
            write_log(label, f"torsion error: {e}")
        try:
            out["real_period"] = float(E.real_period()) if E.real_period() is not None else None
            write_log(label, f"real_period={out['real_period']}")
        except Exception as e:
            write_log(label, f"real_period error: {e}")
    except Exception:
        pass

    write_log(label, "TASK COMPLETE")
    return out

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            task = json.loads(line)
        except Exception as e:
            resp = {"error": f"json_parse_error: {e}", "raw": line}
            sys.stdout.write(json.dumps(resp) + "\n"); sys.stdout.flush()
            continue
        try:
            resp = process_task(task)
        except Exception as e:
            resp = {"label": task.get("label"), "error": "worker_exception", "trace": traceback.format_exc()}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
