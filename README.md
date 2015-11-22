# Hardcopy Backup

Hardcopy Backup generates a printable file that contains an annotated, human-readable, tested backup of data. Humans should be able to read the printed document and reliably reconstruct the data from paper, offline.

The paper backup contains

1. The name of the backed up data
   Date of creation
   Full data checksum
   Data segment checksums
   Restore instructions
   Table of contents
2. User documentation
  - How to restore the data to the application
3. Data segment pages
  - Plaintext
  - Bar codes
    - QR
    - Data matrix

## Uses

- GPG keys
- GPG revocation certs
- SSH keys
- TOTP seeds
- Recovery codes
- Scannable passwords for mobile devices
