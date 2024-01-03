By [@Cypheriel](https://github.com/Cypheriel)

## Install mitmproxy
1. Follow the instructions to [install mitmproxy](https://docs.mitmproxy.org/stable/overview-installation/) and launch either `mitmproxy` or `mitmweb`.
If you plan on sniffing traffic from a macOS VM, it is probably preferable to install mitmproxy on the host OS.
2. Change your proxy settings in macOS to use your local IPv4 address with port 8080 (by default).
    - `System Settings` → `Network` → `Advanced` → `HTTP` *and* `HTTPS` proxies
4. Install the mitmproxy certificate by navigating to http://mitm.it/
5. Disable SSL verification.
    - On mitmweb, this is toggled in `Options` → `Don't verify server certificates`

## Install Frida
1. Install Python
    - **Note**: I would recommend doing so via [pyenv](https://github.com/pyenv/pyenv)
2. `pip3 install frida-tools`

## Download the Frida script
```sh
curl 'https://gist.githubusercontent.com/giantrule/9cf529a4557d6db598a7a390ac023aad/raw/8e7ca86a930d5a03b06d6e69a9dc91cba5fcf33c/disable-ssl-pin.js' > disable-ssl-pinning.js
```

## Disable SIP
Follow the below guide to disable SIP on macOS. This will allow you to attach Frida to system processes.
https://developer.apple.com/documentation/security/disabling_and_enabling_system_integrity_protection

## Attach Frida
```sh
frida -l disable-ssl-pinning.js $NAME_OR_PID
```
Attach Frida to the following services by replacing `$NAME_OR_PID` in the above command with the name or PID of the below services:
- For **iMessage**: `akd`, `imagent`, `IMRemoteURLConnectionAgent`, `identityservicesd`
- For **other** processes I've identified so far: `cloudd`
- **Note**: There appears to be an iCloud process necessary for things like iMessage registration. The only way I know of to find the PID is to use `tcpdump`.

## Mass-attachment Script
Download the attached `attach_frida.sh` script and make it executable via `chmod +x ./attach_frida.sh`.
```sh
curl 'https://gist.githubusercontent.com/Cypheriel/9ffb041a70008be990895f5288880d5e/raw/5fa0ff9db3579e4212bfee66f99370358b92378e/attach_frida.sh' > attach_frida.sh
chmod +x attach_frida.sh
```
Then, provide the list of processes to attach to like so:
```sh
sudo ./attach_frida.sh akd imagent IMRemoteURLConnectionAgent
```

## Finishing Notes
Now, you should be able to sniff macOS traffic including that from internal services with ease.
In the case of iMessage, if you get an error along the lines of "There was a problem connecting to the server" when signing in, please try rebooting macOS and try again.
For registration data, sign out of iMessage before attempting to capture data.
If the service you are trying to investigate is not listed above, take a look through `sudo tcpdump -k PN` to see which processes you need to attach to.