# Upstream Notice — ECC

The ECC project is maintained by Affaan Mustafa:

https://github.com/affaan-m/ECC

ECC currently declares the MIT License in its package/plugin metadata.

This prototype does not claim ownership of ECC. If ECC-derived files are later copied, vendored, or redistributed here, the original copyright and MIT license notice must be retained and the copied files must remain identifiable as upstream-derived material.

Third-party dependencies used by ECC are not automatically covered by the ECC MIT license. A future vendored distribution must generate and review a third-party license inventory before release.

## Planned provenance model

```text
upstream ECC
    ↓
version / commit recorded
    ↓
ECC-derived tree (if vendored)
    + original notices
    ↓
Shirakami adapter
    ↓
Shirakami runtime boundary
```

Until that provenance-preserving vendoring step is implemented, this repository contains only the adapter contract and integration documentation.
