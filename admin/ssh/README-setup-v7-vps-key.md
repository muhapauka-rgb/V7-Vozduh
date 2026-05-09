# V7 VPS SSH key setup

Local private key:

`/Users/ponch/.ssh/v7_vps_ed25519`

Public key file in project:

`/Users/ponch/V7 Vozduh/Проект/admin/ssh/v7-vps-public-key.pub`

Run this once on the VPS as root, for example through the hosting provider console:

```bash
mkdir -p /root/.ssh
chmod 700 /root/.ssh
printf '%s\n' 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIL7UYigRkDXFPVguLEe4lyAA+P5NgJLS7QVtHviV3UGa v7-vps-195.2.79.116-20260509' >> /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
```

After that, local access should work with:

```bash
ssh v7-vps
```

This file contains only the public key. Do not place the private key inside the project repository.
