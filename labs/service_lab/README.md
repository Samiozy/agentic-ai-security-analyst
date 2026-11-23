# Service lab — Partner A

Use Metasploitable 2 **on a local x86 VM with a host-only adapter**, or another
instructor-approved vulnerable service image. Do not bridge this VM to the
internet or publish it publicly. Jetstream2 is for the model, not the VM.

1. Obtain the lab VM from its official distribution and isolate the VM network.
2. Determine its *actual* host-only IP using the VM console (`ip addr`).
3. Edit `guardrails/targets.json` replacing example `192.168.56.101` with that IP,
   and list only ports you approve for testing.
4. From host, run `python cli.py --mode collect --domain service --target
   YOUR_VM_IP --ports 21,22,80` (use one command line; replace YOUR_VM_IP).
5. Type `APPROVE` separately for each action. Record open ports, banner and FTP
   results; do not run exploit modules. If FTP does not exist, select an
   instructor-approved local service target with FTP and record the limitation.

Do **not** treat version matches as proof of a vulnerability. Consult original
vendor advisories and document supported versus unsupported claims.
