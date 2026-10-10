"""MolStructBench scoring-only edition; no Solver execution dependency."""
import argparse,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main(argv=None):
    parser=argparse.ArgumentParser(prog='molstructbench',description='Data + official local scorer edition. Solver execution is provided only in the with-Harness edition.')
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('score');p.add_argument('--predictions',required=True);p.add_argument('--output',required=True);p.add_argument('--judge-cache',action='append',default=[]);p.add_argument('--offline',action='store_true');p.add_argument('--resume',action='store_true')
    a=parser.parse_args(argv)
    try:
        from scibench.local_score import score_local
        result=score_local(a.predictions,a.output,a.judge_cache,a.offline)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 3 if result['pending_count'] else 0
    except Exception as exc:parser.exit(2,type(exc).__name__+': '+str(exc)+'\n')
if __name__=='__main__':raise SystemExit(main())
