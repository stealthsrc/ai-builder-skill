# Unsafe To Safe

This file gives one compact example per builder category so users can see the style of hardening the skill is expected to apply.

---

## PowerShell

Unsafe:

```powershell
Invoke-Expression "ping $userInput"
```

Safer:

```powershell
& ping.exe $validatedHost
```

Why:

- avoids dynamic evaluation
- passes arguments directly
- makes validation practical before execution

---

## Python

Unsafe:

```python
subprocess.run(user_input, shell=True)
```

Safer:

```python
subprocess.run(["ping", validated_host], check=True)
```

Why:

- no shell expansion
- argument boundaries stay explicit

---

## VBA

Unsafe:

```vb
Shell "cmd.exe /c " & userInput
```

Safer:

```vb
' Prefer internal workbook logic or a controlled helper process.
' Validate any cell value before it reaches a file path, command, or email field.
```

Why:

- VBA is especially risky when it starts external processes with unvalidated values
- many business users will run macros with more trust than they should
