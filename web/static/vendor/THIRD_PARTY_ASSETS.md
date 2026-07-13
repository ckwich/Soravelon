# Vendored browser assets

These production browser assets are copied without modification from the named
npm packages. Soravelon serves them locally so the public site and stock
webclient do not depend on third-party CDNs at runtime.

| Asset | npm source | License | SHA-256 |
| --- | --- | --- | --- |
| `jquery-3.7.1.min.js` | `jquery@3.7.1` | MIT (`jquery-3.7.1-LICENSE.txt`) | `fc9a93dd241f6b045cbff0481cf4e1901becd0e12fb45166a8f17f95823f0b1a` |
| `bootstrap-4.6.2.min.css` | `bootstrap@4.6.2` | MIT (`bootstrap-4.6.2-LICENSE.txt`) | `f886516f3d41e9e7bd994c7f7a39a89cafae9483f90396cb0ddeafe8d1ea5e72` |
| `bootstrap-4.6.2.bundle.min.js` | `bootstrap@4.6.2` | MIT (`bootstrap-4.6.2-LICENSE.txt`) | `19126b874a32753d42c12dfa6c17892bfd93820a5a5100ba1b34da4d07599b49` |
| `goldenlayout-1.5.9.min.js` | `golden-layout@1.5.9` | MIT (`goldenlayout-1.5.9-LICENSE.txt`) | `3612406437c682fe0f881f865654ab3dd877b9cef95d7612338b2ef218137212` |
| `goldenlayout-1.5.9-base.css` | `golden-layout@1.5.9` | MIT (`goldenlayout-1.5.9-LICENSE.txt`) | `a080d1d7cc8a159b5f8c225f0ec258a5306fd52f509b1628a5eab0d9d3bdeb13` |
| `goldenlayout-1.5.9-dark-theme.css` | `golden-layout@1.5.9` | MIT (`goldenlayout-1.5.9-LICENSE.txt`) | `ca0c3c3ef4832495062dfe90f4a210b1847798e9a240d9436b130b0cec7dc4bd` |
| `favico-0.3.10.min.js` | `favico.js@0.3.10` | MIT (`favico-0.3.10-LICENSE.txt`) | `691a2eafc9720268bb1bdb52728c307f5dd9752eb06c3c213026faa39fe830b0` |

The package tarballs were retrieved from the npm registry on 2026-07-13. npm
verified each package's published `dist.integrity` while packing it. Upgrade by
retrieving an explicit version, copying only the production files and license,
updating this table, and rerunning `tests.test_public_web_surface` plus the live
browser and protocol gates.
