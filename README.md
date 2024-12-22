![Carnac_AARuPCSy7K](https://github.com/user-attachments/assets/a84e1f2a-fe3f-498c-a038-da7ea2f19306)




# Remote Shutdown Guide

This guide details how to remotely shut down a computer using various methods and programming scripts across Windows, Python, and Bash.

---

## 1. **Using Command Line on Windows**

### Syntax:
```bash
shutdown /s /t <time_in_seconds> /m \\<remote_computer_name_or_IP> /c "<message>" /f
```

### Explanation of Parameters:
- `/s` - Initiates a shutdown.
- `/t <time_in_seconds>` - Sets a timer before shutdown. Default is 30 seconds.
- `/m \\<remote_computer_name_or_IP>` - Specifies the target computer.
- `/c "<message>"` - Displays a custom message before shutdown.
- `/f` - Forces applications to close without warning.

### Example:
Shutdown a remote computer (IP: 192.168.1.100) immediately:
```bash
shutdown /s /t 0 /m \\192.168.1.100 /c "System maintenance" /f
```

### Requirements:
- Remote computer must allow remote shutdowns.
- Proper permissions and network configuration (e.g., open RPC ports).

---

## 2. **Using Python for Shutdown**

Python provides an easy and scriptable way to initiate a shutdown. Below are two examples:

### Local Shutdown:
```python
import os
os.system("shutdown /s /t 0")
```
This command performs an immediate local shutdown.

### Remote Shutdown:
```python
import os
remote_computer = "192.168.1.100"
os.system(f"shutdown /s /m \\\\"{remote_computer}\\\\" /t 0 /f")
```

### Notes:
- Python scripts must be run with appropriate privileges.
- Ensure the remote computer is configured for remote administration.

---

## 3. **Using Bash Script for Linux Systems**

### Local Shutdown:
```bash
#!/bin/bash
shutdown now
```
This shuts down the local Linux system immediately.

### Remote Shutdown via SSH:
```bash
#!/bin/bash
ssh user@192.168.1.100 "sudo shutdown now"
```

### Notes:
- Ensure SSH access is enabled on the remote system.
- SSH keys can be configured to avoid password prompts.

---

## 4. **Remote Configuration and Security Tips**
- Enable Remote Administration:
  - On Windows, execute:
    ```bash
    netsh advfirewall firewall set rule group="Remote Administration" new enable=yes
    ```

- Configure BIOS/UEFI for Wake-on-LAN if needed.
- Use secure networks to prevent unauthorized shutdowns.

---

## Visual Overview

![Remote Shutdown](https://github.com/user-attachments/assets/a84e1f2a-fe3f-498c-a038-da7ea2f19306)

---

For more examples and advanced usage, check out [GitHub Gist Repository](https://github.com/shikakker/Shutdown).
