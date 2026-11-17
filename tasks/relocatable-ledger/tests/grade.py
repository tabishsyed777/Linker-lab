"""Outcome verifier. Candidate build/run processes drop to an unprivileged user."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def expected_quote(cents,quantity):
    return cents*quantity+7


def matches_quote(returncode,stdout,cents,quantity):
    return returncode==0 and stdout==f'{expected_quote(cents,quantity)}\n'


def command(args,**kwargs):
    return subprocess.run(['/usr/sbin/runuser','-u','builder','--',*map(str,args)],capture_output=True,text=True,timeout=35,
                          env={'PATH':'/usr/bin:/bin','HOME':'/tmp','LANG':'C'},**kwargs)


def evaluate():
    checks=[]
    def check(name,passed,detail=''):
        checks.append({'name':name,'passed':bool(passed),'detail':str(detail)[-2500:]})
    with tempfile.TemporaryDirectory(prefix='linker-grade-') as temporary:
        root=Path(temporary)
        root.chmod(0o755)
        build=root/'build'; build.mkdir(); build.chmod(0o777)
        prefix=root/'install'; prefix.mkdir(); prefix.chmod(0o777)
        result=command(['cmake','-S','/app/project','-B',build,f'-DCMAKE_INSTALL_PREFIX={prefix}'])
        check('clean_configure',result.returncode==0,result.stderr)
        if result.returncode:
            return {'passed':False,'checks':checks}
        result=command(['cmake','--build',build,'--parallel','2'])
        check('clean_build',result.returncode==0,result.stderr)
        if result.returncode:
            return {'passed':False,'checks':checks}
        result=command(['cmake','--install',build])
        check('install',result.returncode==0,result.stderr)
        if result.returncode:
            return {'passed':False,'checks':checks}
        relocated=root/'unrelated release with spaces'
        shutil.copytree(prefix,relocated)
        shutil.rmtree(prefix)
        shutil.rmtree(build)
        exe=relocated/'bin/ledgercalc'; ledger=relocated/'lib/libledger.so'; money=relocated/'lib/libmoney.so'
        for name,file in [('executable',exe),('ledger_library',ledger),('money_library',money)]:
            check(name,file.is_file() and not file.is_symlink())
        if not all(file.is_file() for file in [exe,ledger,money]):
            return {'passed':False,'checks':checks}
        for file,needed,label in [(exe,'libledger.so','executable_dynamic_dependency'),(ledger,'libmoney.so','transitive_dynamic_dependency')]:
            inspected=subprocess.run(['readelf','-d',str(file)],capture_output=True,text=True,timeout=5)
            check(label,inspected.returncode==0 and any('NEEDED' in line and f'[{needed}]' in line for line in inspected.stdout.splitlines()),inspected.stdout)
        for index,(cents,quantity) in enumerate([(125,3),(0,0),(-20,4),(1000000,10000),(913,17),(37,19)]):
            result=command([exe,str(cents),str(quantity)],cwd='/')
            check(f'relocated_quote_{index}',matches_quote(result.returncode,result.stdout,cents,quantity),result.stdout+result.stderr)
        for index,args in enumerate([[],['bad','2'],['3','-1']]):
            result=command([exe,*args],cwd='/')
            check(f'invalid_arguments_{index}',result.returncode==2)
    return {'passed':all(item['passed'] for item in checks),'checks':checks}


def main():
    try:
        report=evaluate()
    except Exception as error:
        report={'passed':False,'checks':[{'name':'verifier_execution','passed':False,'detail':str(error)}]}
    directory=Path('/logs/verifier'); directory.mkdir(parents=True,exist_ok=True)
    directory.chmod(0o700)
    (directory/'details.json').write_text(json.dumps(report,indent=2)+'\n')
    (directory/'reward.txt').write_text('1\n' if report['passed'] else '0\n')
    print(json.dumps(report))


if __name__=='__main__':
    main()
