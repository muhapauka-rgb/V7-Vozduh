# Z9 Evidence 03 - Live Access Gate

## Production Host Candidate

Prior project documentation identifies the VPS as:

```text
195.2.79.116
v3119922.hosted-by-vdsina.ru
```

## Read-Only SSH Check Attempt

Attempted non-interactive key-based read-only command:

```text
ssh -o BatchMode=yes -o ConnectTimeout=10 root@195.2.79.116 'hostname; date -Is; test -d /opt/v7 && echo opt_v7_present || echo opt_v7_missing'
```

Result:

```text
Permission denied (publickey,password).
```

## Interactive Root SSH Attempt

An interactive password-authenticated root SSH session was not used. The environment rejected it as too broad for production access without a read-only command bound.

## Live Gate Verdict

Live runtime was not revalidated.

Blocked checks:

- production branch
- production commit
- production runtime state
- production systemd service/timer status
- production restore barrier state
- production selected move generation
- production operation envelope
- production audit path
- production closure path
- production rollback path

Z9 absolute rule requires STOP when live reality cannot be confirmed.

