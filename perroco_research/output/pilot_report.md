# Perroco Lab — Piloto de investigación automatizada (20 materiales)

Resultado del pipeline RAW SOURCE → EXTRACTED CLAIM → NORMALISED CLAIM → VALIDATION → PROPOSED CHANGE. **El master no se ha modificado.** Todas las propuestas están en `output/proposed_changes.jsonl`.

Fecha de ejecución: 2026-09-28 · master analizado (sha256): `3a626dedfa9d0e6c…` · estados posibles por material: NOT_STARTED → SEARCHING → SOURCES_FOUND → EXTRACTED → NEEDS_REVIEW / VALIDATED / NO_PUBLIC_DATA_FOUND / ERROR.

## Resumen global

| Indicador | Valor |
|---|---|
| Queries realizadas | 180 (claude_websearch: 153, pubchem_api: 21, ncbi_pmc_api: 6) |
| URLs distintas encontradas | 992 |
| URLs cuya descarga se intentó | 410 (MANUAL_RETRIEVAL_REQUIRED: 73, ROBOTS_DISALLOWED: 86, FETCHED: 230, HTTP_ERROR: 1, ENV_UNREACHABLE: 19, UNSUPPORTED_CONTENT: 1) |
| Documentos descargados (web) | 229 (xml: 59, html: 147, pdf: 82 incl. API) |
| Respuestas de API guardadas (PubChem/PMC) | 59 |
| Materiales con datos nuevos | 17: S-0486, S-0526, S-0479, S-0024, S-0518, S-0372, S-0502, S-0366, N-0775, N-0697, N-0623, N-0632, N-0556, N-0728, S-0507, S-0023, S-0020 |
| Materiales sin resultados útiles | 3: S-0002, S-0468, S-0508 |
| Duplicados exactos (mismo hash, varias URLs) | 9 |
| Casi-duplicados / copias derivadas | 5 / 1 |
| Conflictos detectados | 29 |
| Nuevos registros de dosis de fabricante | {'AUTO_ELIGIBLE': 1, 'NEEDS_REVIEW': 2, 'BLOCKED_CONFLICT': 0} |
| Nuevos registros de dosis secundaria (distribuidor/retailer) | 7 |
| Nuevos registros de presión de vapor | {'AUTO_ELIGIBLE': 0, 'NEEDS_REVIEW': 5, 'BLOCKED_CONFLICT': 3} |
| Nuevos registros físico-químicos (total) | 47 |
| Nuevos registros de performance | {'AUTO_ELIGIBLE': 1, 'NEEDS_REVIEW': 10, 'BLOCKED_CONFLICT': 2} |
| Mejoras de identidad propuestas | 11 |
| Nuevos SDS/CLP | 28 |
| Filas de composición de referencia GC-MS | 44 filas (de 38 estudios localizados) |
| Cambios propuestos por estado | {'NEEDS_REVIEW': 154, 'BLOCKED_CONFLICT': 10, 'AUTO_ELIGIBLE': 10} |
| Estados finales de materiales | {'NO_PUBLIC_DATA_FOUND': 3, 'NEEDS_REVIEW': 17} |

## Estimación de precisión (auditoría manual de una muestra)

**Propuestas AUTO_ELIGIBLE: 10/10 correctas (100 %, n pequeña).** Claims extraídos: 88,6 % (62/70) en la muestra 1 y 87,5 % (49/56) en la muestra 2; propuestas de revisión: 80 % (32/40). Todos los tipos de error encontrados se corrigieron y el piloto se re-ejecutó; la precisión tras la última ronda no se ha re-medido con una muestra nueva, por lo que la estimación prudente para claims no automáticos es **~85–90 %**, y por eso siguen marcados NEEDS_REVIEW. Aparte de la extracción, varias fuentes (retailers, agregadores tipo ChemicalBook/LookChem) publican valores dudosos: se leen fielmente pero se marcan como evidencia secundaria y suelen acabar en CONFLICT. Detalle: data/audit/audit_verdicts.json.

## ¿Qué cambiaría en READY / PARTIAL / NOT_READY? (estimación)

Recalculado con los pesos y topes documentados en FORMULATION READINESS; es una estimación, no el recálculo del workbook.

| Clase | Antes (master) | Solo AUTO_ELIGIBLE | Si se aprueban también NEEDS_REVIEW |
|---|---|---|---|
| READY_WITH_CAVEATS | 2 | 2 | 2 |
| PARTIAL | 7 | 8 | 9 |
| NOT_READY | 11 | 10 | 9 |

| Material | Antes | Clase | Tras AUTO | Clase | Tras todo | Clase |
|---|---|---|---|---|---|---|
| S-0372 | 74 | READY_WITH_CAVEATS | 81 | READY_WITH_CAVEATS | 81 | READY_WITH_CAVEATS |
| S-0502 | 41 | NOT_READY | 61 | PARTIAL | 61 | PARTIAL |
| N-0697 | 36 | NOT_READY | 36 | NOT_READY | 38 | NOT_READY |
| N-0556 | 55 | PARTIAL | 55 | PARTIAL | 57 | PARTIAL |
| N-0728 | 18 | NOT_READY | 18 | NOT_READY | 20 | NOT_READY |
| S-0507 | 0 | NOT_READY | 0 | NOT_READY | 20 | NOT_READY |
| S-0023 | 20 | NOT_READY | 20 | NOT_READY | 50 | PARTIAL |
| S-0020 | 0 | NOT_READY | 0 | NOT_READY | 33 | NOT_READY |

## Dominios inaccesibles (no se evadió ningún bloqueo)

| Dominio | Estado | URLs | Motivo |
|---|---|---|---|
| thegoodscentscompany.com | ROBOTS_DISALLOWED | 12 | robots.txt disallows ClaudeBot for /data/ab1005391.html -> MANUAL_RETRIEVAL_REQUIRED |
| scentree.co | ROBOTS_DISALLOWED | 4 | robots.txt disallows ClaudeBot for /en/Muscenone%C2%AE.html -> MANUAL_RETRIEVAL_REQUIRED |
| fragrantica.com | ROBOTS_DISALLOWED | 3 | robots.txt disallows ClaudeBot for /notes/Amber-Xtreme-879.html -> MANUAL_RETRIEVAL_REQUI… |
| iff.com | MANUAL_RETRIEVAL_REQUIRED | 2 | HTTP 403 (site refuses automated access; not bypassed) |
| chemicalbook.com | MANUAL_RETRIEVAL_REQUIRED | 2 | HTTP 429 (site refuses automated access; not bypassed) |
| tandfonline.com | MANUAL_RETRIEVAL_REQUIRED | 2 | HTTP 403 (site refuses automated access; not bypassed) |
| ulprospector.com | MANUAL_RETRIEVAL_REQUIRED | 2 | HTTP 403 (site refuses automated access; not bypassed) |
| scribd.com | ROBOTS_DISALLOWED | 2 | robots.txt disallows ClaudeBot for /document/710633645/Iso-E-Super-SDS -> MANUAL_RETRIEVA… |
| researchgate.net | MANUAL_RETRIEVAL_REQUIRED | 2 | HTTP 403 (site refuses automated access; not bypassed) |
| creatingperfume.com | ENV_UNREACHABLE | 2 | domain unreachable earlier in run: robots.txt unreachable: HTTPSConnectionPool(host='www.… |
| specialchem.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| lmrnaturals.iff.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| firmenich.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| cosmetics.specialchem.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| datasheets.scbt.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| studio.dsm-firmenich.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| sciencedirect.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| labelsds.com | ROBOTS_DISALLOWED | 1 | robots.txt disallows PerrocoLabResearchBot for /images/user_uploads/Tim-bor%20Label%204-1… |
| sds.rentokil-initial.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| scijournals.onlinelibrary.wiley.com | MANUAL_RETRIEVAL_REQUIRED | 1 | HTTP 403 (site refuses automated access; not bypassed) |
| manuals.plus | MANUAL_RETRIEVAL_REQUIRED | 1 | HTTP 403 (site refuses automated access; not bypassed) |
| givaudan.com | MANUAL_RETRIEVAL_REQUIRED | 1 | CAPTCHA page served (HTTP 200) - bot protection; not bypassed |
| doi.org | MANUAL_RETRIEVAL_REQUIRED | 1 | HTTP 403 (site refuses automated access; not bypassed) |
| basenotes.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| lmrnaturals.iff.com | ENV_UNREACHABLE | 1 | domain unreachable earlier in run: robots.txt unreachable: ('Connection aborted.', Connec… |
| t3db.ca | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| pim-resources.coleparmer.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| pellwall.com | ENV_UNREACHABLE | 1 | domain unreachable earlier in run: robots.txt unreachable: HTTPSConnectionPool(host='pell… |
| fishersci.com | ENV_UNREACHABLE | 1 | robots.txt unreachable: HTTPSConnectionPool(host='www.fishersci.com', port=443): Read tim… |
| biosynth.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| olaughlinco.com | ENV_UNREACHABLE | 1 | domain unreachable earlier in run: ConnectionError: HTTPConnectionPool(host='olaughlinco.… |
| ir.iff.com | ENV_UNREACHABLE | 1 | domain unreachable earlier in run: robots.txt unreachable: HTTPSConnectionPool(host='ir.i… |
| carlroth.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| data.aromatics.com | MANUAL_RETRIEVAL_REQUIRED | 1 | HTTP 429 (site refuses automated access; not bypassed) |
| sigmaaldrich.com | ENV_UNREACHABLE | 1 | robots.txt unreachable: HTTPSConnectionPool(host='www.sigmaaldrich.com', port=443): Read … |
| spectrumchemical.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| ouddict.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| ultranl.com | ENV_UNREACHABLE | 1 | robots.txt unreachable: HTTPSConnectionPool(host='ultranl.com', port=443): Max retries ex… |
| cdn.planttherapy.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| dam.hollandandbarrettimages.co.uk | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| aroma-zone.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| ewg.org | MANUAL_RETRIEVAL_REQUIRED | 1 | HTTP 403 (site refuses automated access; not bypassed) |
| efsa.onlinelibrary.wiley.com | MANUAL_RETRIEVAL_REQUIRED | 1 | HTTP 403 (site refuses automated access; not bypassed) |
| avenalab.com | ENV_UNREACHABLE | 1 | domain unreachable earlier in run: robots.txt unreachable: ('Connection aborted.', Connec… |
| m.molbase.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| myskinrecipes.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |
| perfumerflavorist.com | ROBOTS_DISALLOWED | 1 | robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ… |

## Conflictos

| Material | Campo | Detalle | ¿Contra el master? |
|---|---|---|---|
| S-0486 | flash_point | flash_point: independent sources disagree beyond tolerance ('abs', 6) | no |
| S-0486 | h_statement | SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] | no |
| S-0526 | density | density: independent sources disagree beyond tolerance ('abs', 0.012) | no |
| S-0479 | boiling_point | boiling_point: independent sources disagree beyond tolerance ('abs', 8) [lower-tier dissent only] | no |
| S-0479 | h_statement | SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] | no |
| S-0518 | h_statement | SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] | no |
| S-0372 | vapour_pressure | vapour_pressure: independent sources disagree beyond tolerance ('rel', 0.3) [lower-tier dissent only] | no |
| S-0372 | flash_point | flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only] | no |
| S-0372 | logp | logp: independent sources disagree beyond tolerance ('abs', 0.6) [lower-tier dissent only] | no |
| S-0372 | use_level | recommended use levels from independent sources do not agree [lower-tier dissent only] | no |
| S-0366 | vapour_pressure | vapour_pressure: independent sources disagree beyond tolerance ('rel', 0.3) | no |
| S-0366 | flash_point | flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only] | no |
| S-0366 | boiling_point | boiling_point: independent sources disagree beyond tolerance ('abs', 8) [lower-tier dissent only] | no |
| N-0775 | cas | source CAS not in master CAS set | sí |
| N-0775 | h_statement | SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] | no |
| N-0697 | density | density: independent sources disagree beyond tolerance ('abs', 0.012) | no |
| N-0697 | flash_point | flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only] | no |
| N-0697 | cas | source CAS not in master CAS set | sí |
| N-0697 | h_statement | SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] | no |
| N-0623 | h_statement | SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] | no |
| N-0632 | flash_point | flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only] | no |
| N-0632 | cas | source CAS not in master CAS set | sí |
| N-0632 | h_statement | SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] | no |
| N-0556 | cas | source CAS not in master CAS set | sí |
| N-0728 | cas | source CAS not in master CAS set | sí |
| N-0728 | botanical_species | sources identify polianthes tuberosa; master says 'Rosa x damascena (typical source; not stated for all grades)' | sí |
| N-0728 | h_statement | SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] | no |
| S-0020 | flash_point | flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only] | no |
| S-0020 | tenacity | tenacity: independent sources disagree beyond tolerance ('rel', 0.5) | no |

## Mejoras de identidad propuestas

| Material | Columna | Antes | Propuesto | Estado |
|---|---|---|---|---|
| S-0372 | identity_tier | B_EXACT_CHEMICAL_GRADE_UNCONFIRMED | A_EXACT_COMMERCIAL_GRADE | AUTO_ELIGIBLE |
| S-0372 | supplier_grade_url |  | https://www.givaudan.com/fragrance-beauty/fragrance-ingredients-business/fragrance-molecules/florhydraltm | AUTO_ELIGIBLE |
| S-0502 | identity_tier | B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK | A_EXACT_COMMERCIAL_GRADE | AUTO_ELIGIBLE |
| S-0502 | supplier_grade_url |  | https://www.symrise.com/fileadmin/symrise/Marketing/Scent_and_care/Aroma_molecules/Ingredient_finder/SYM_PC_Datenblaetter/SYM_PC-Timberol.pdf | AUTO_ELIGIBLE |
| N-0728 | botanical_species | Rosa x damascena (typical source; not stated for all grades) | polianthes tuberosa | BLOCKED_CONFLICT |
| S-0507 | resolved_cas |  | 476332-65-7 | NEEDS_REVIEW |
| S-0507 | identity_tier | D_FAMILY_LEVEL_ONLY | B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK | NEEDS_REVIEW |
| S-0023 | resolved_cas |  | 82461-14-1 | NEEDS_REVIEW |
| S-0023 | identity_tier | D_FAMILY_LEVEL_ONLY | B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK | NEEDS_REVIEW |
| S-0020 | resolved_cas |  | 1337-83-3 | NEEDS_REVIEW |
| S-0020 | identity_tier | D_FAMILY_LEVEL_ONLY | B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK | NEEDS_REVIEW |

## SDS / CLP

| Material | Clasificación | Fuente | Estado |
|---|---|---|---|
| S-0486 |  / H: H315, H319, H411 | https://media.knowde.com/image/upload/v1731934339/10341-01Bacdanol_SDSEUEN.pdf20241118-1-8n7ky9.pdf | NEEDS_REVIEW |
| S-0486 |  / H: EUH208, H315, H319, H411 | https://www.hekserij.nl/wp-content/uploads/2024/10/SDS-23144-Bacdanol-IFF-2024-05.pdf | NEEDS_REVIEW |
| S-0486 |  / H: H319, H410 | https://shop.perfumersapprentice.com/msds/9237.pdf | NEEDS_REVIEW |
| S-0486 | Aquatic Acute 1; Aquatic Chronic 1; Eye Irrit. 2A; Skin Irrit. 2 / H: H315, H319, H400, H410 | https://www.chemtexusa.com/wp-content/uploads/2021/03/B1000_Bacdanol.pdf | NEEDS_REVIEW |
| S-0526 |  / H: H317, H400, H410 | https://finefrag.com/wp-content/uploads/2020/06/MUSCEMOR-MSDS.pdf | NEEDS_REVIEW |
| S-0479 |  / H: H315, H317, H400, H410 | https://www.hekserij.nl/wp-content/uploads/2025/03/SDS-23021-Iso-E-Super-IFF-2025-03.pdf | NEEDS_REVIEW |
| S-0479 | Aquatic Acute 2; Skin Irrit. 2; Skin Sens. 1 / H: H315, H317, H401 | https://www.chemtexusa.com/wp-content/uploads/2021/03/I2200_IsoESuper.pdf | NEEDS_REVIEW |
| S-0479 |  / H: H315, H317 | https://perfumersupplyhouse.com/wp-content/uploads/2019/06/ISO-E-SUPER-GHS-SDS.pdf | NEEDS_REVIEW |
| S-0479 |  / H: H315, H317, H401, H411 | http://www.mu-intel.com/upload/msds/20180320232644.pdf | NEEDS_REVIEW |
| S-0479 |  / H: H315, H317, H401, H410 | https://finefrag.com/wp-content/uploads/2019/11/ISO-E-SUPER_00098663_GHS_MSDS_17SEP2019_112130.pdf | NEEDS_REVIEW |
| S-0024 | Acute Tox. 5; Aquatic Acute 2; Aquatic Chronic 2 / H: H303, H401, H411 | https://image.makewebeasy.net/makeweb/0/oCmFYX9sp/Document/Rhubofix_SDS.pdf?v=202405291424 | NEEDS_REVIEW |
| S-0518 |  / H: H303, H313, H400, H410 | https://shop.perfumersapprentice.com/Images/HabanolideSDS.pdf | NEEDS_REVIEW |
| S-0518 |  / H: H303, H313, H410 | https://shop.perfumersapprentice.com/msds/6099.pdf | NEEDS_REVIEW |
| S-0372 | Aquatic Acute 2; Aquatic Chronic 2; Flam. Liq. 4 / H: H227, H401, H411 | https://www.vigon.com/product/florhydral/?doc=PACKET%2F501126packet.pdf&namee=FlorhydralAllDocuments | NEEDS_REVIEW |
| S-0366 | Eye Dam. 1; STOT SE 3; Skin Corr. 1B / H: H314, H318, H336 | https://www.vigon.com/product/calone-1951/?doc=PACKET/503181packet.pdf&namee=Calone1951AllDocuments | NEEDS_REVIEW |
| N-0775 |  / H: H317 | https://cdn.accentuate.io/1800375107643/1592454388521/Vetiver---Material-Safety--Data-Sheet.pdf?v=0 | NEEDS_REVIEW |
| N-0775 |  / H: H304, H315, H317, H411 | https://nikura.blob.core.windows.net/pdfs/Safety_Data_Sheet_Vetiver_Essential_Oil_EO-VET.pdf | NEEDS_REVIEW |
| N-0697 | Aquatic Acute 2; Aquatic Chronic 2; Asp. Tox. 1; Carc. 2; Muta. 2; Skin Irrit. 2; Skin Sens. 1 / H: H304, H313, H315, H317, H318, H341, H351, H401, H411 | https://ultrainternational.com/wp-content/uploads/2023/08/SDS-ROSE-OIL.pdf | NEEDS_REVIEW |
| N-0697 |  / H: H226, H303, H315, H317, H318, H341, H351, H401, H412 | https://finefrag.com/wp-content/uploads/2020/06/ROSE-OIL-TURKISH-LMR_00181102_GHS_SDS_28May2020_482142.pdf | NEEDS_REVIEW |
| N-0623 |  / H: H227, H315 | https://cdn.accentuate.io/1871053684795/1619828099392/Clary-Sage---Material-Safety--Data-Sheet.pdf?v=0 | NEEDS_REVIEW |
| N-0623 |  / H: H315, H317, H319, H402, H412 | https://docs.newdirectionsaromatics.com/msds/SDS_ClarySageOrganicEO.pdf | NEEDS_REVIEW |
| N-0632 |  / H: H226, H304, H315, H317, H319, H411 | https://www.nhrorganicoils.com/uploads/20221122161304e_Cardamom_SDS.pdf | NEEDS_REVIEW |
| N-0632 |  / H: H227, H303, H315, H317, H319, H411 | https://finefrag.com/wp-content/uploads/2020/06/CARDAMOM-OIL-GUATEMALA-LMR_00032885_GHS_SDS_28May2020_482080.pdf | NEEDS_REVIEW |
| N-0632 | Aquatic Acute 2; Aquatic Chronic 2; Asp. Tox. 1; Eye Irrit. 2A; Flam. Liq. 3; Skin Irrit. 2; Skin Sens. 1 / H: H226, H304, H315, H317, H319, H401, H411 | http://ultrainternational.com/wp-content/uploads/2023/08/SDS-CARDAMOM-OIL.pdf | NEEDS_REVIEW |
| N-0556 |  / H: H226, H302, H304, H314, H315, H317, H410, H411 | https://www.nhrorganicoils.com/uploads/20160817124803e_Bergamot_Bergapten_Free_SDS.pdf | NEEDS_REVIEW |
| N-0728 | Aquatic Acute 3; Aquatic Chronic 3 / H: H317, H332, H402, H412 | https://shop.perfumersapprentice.com/msds/9309.pdf | NEEDS_REVIEW |
| N-0728 |  / H: H302, H317, H332, H412 | https://www.echemi.com/sds/tuberoseabsolute-pid_Rock27439.html | NEEDS_REVIEW |
| S-0507 |  / H: H317, H411 | https://www.scentspiracy.com/fragrance-ingredients/p/amberxtreme | NEEDS_REVIEW |

## Errores

_Ninguno._

## Tabla por material

| ID | Material | Estado | Docs aceptados | Identidad | Conflictos | Cambios auto/revisión/bloq. | Readiness antes→después(auto) |
|---|---|---|---|---|---|---|---|
| S-0002 | VERBENAL | NO_PUBLIC_DATA_FOUND | 1 | EXACT_CAS_ONLY | 0 | 0/1/0 | 33 → 33 |
| S-0468 | HEALINGWOOD | NO_PUBLIC_DATA_FOUND | 2 | LIKELY_MATCH | 0 | 0/1/0 | 40 → 40 |
| S-0486 | BACDANOL TOCO | NEEDS_REVIEW | 12 | EXACT_NAME_MANUFACTURER | 2 | 0/13/2 | 61 → 61 |
| S-0526 | MUSCEMOR (ELINCS) | NEEDS_REVIEW | 7 | EXACT_NAME_MANUFACTURER | 1 | 0/4/0 | 49 → 49 |
| S-0479 | ISO E SUPER TOCO | NEEDS_REVIEW | 14 | EXACT_NAME_MANUFACTURER | 2 | 0/10/0 | 89 → 89 |
| S-0024 | RHUBOFIX FIRM | NEEDS_REVIEW | 11 | EXACT_NAME_MANUFACTURER | 0 | 0/3/0 | 50 → 50 |
| S-0518 | HABANOLIDE (ELINCS) | NEEDS_REVIEW | 9 | EXACT_NAME_MANUFACTURER | 1 | 0/7/0 | 60 → 60 |
| S-0372 | FLORHYDRAL TOCO (ELINCS) | NEEDS_REVIEW | 13 | EXACT_GRADE | 4 | 5/15/3 | 74 → 81 |
| S-0502 | TIMBEROL | NEEDS_REVIEW | 9 | EXACT_GRADE | 0 | 5/3/0 | 41 → 61 |
| S-0366 | CALONE | NEEDS_REVIEW | 11 | EXACT_NAME_MANUFACTURER | 3 | 0/12/2 | 48 → 48 |
| N-0775 | VETIVER OIL LMR | NEEDS_REVIEW | 16 | LIKELY_MATCH | 2 | 0/5/0 | 48 → 48 |
| N-0697 | ROSE OIL TURKISH LMR | NEEDS_REVIEW | 15 | LIKELY_MATCH | 4 | 0/14/0 | 36 → 36 |
| N-0623 | SAGE CLARY OIL FRENCH LMR | NEEDS_REVIEW | 14 | LIKELY_MATCH | 1 | 0/16/0 | 36 → 36 |
| N-0632 | CARDAMOM OIL EI LMR | NEEDS_REVIEW | 16 | LIKELY_MATCH | 3 | 0/14/0 | 36 → 36 |
| N-0556 | BERGAMOT OIL DEFUROCOUMARI NIZED | NEEDS_REVIEW | 14 | LIKELY_MATCH | 1 | 0/13/0 | 55 → 55 |
| N-0728 | TUBEROSE ABS INDIA LMR | NEEDS_REVIEW | 12 | LIKELY_MATCH | 3 | 0/4/1 | 18 → 18 |
| S-0507 | AMBER XTREME TM | NEEDS_REVIEW | 5 | LIKELY_MATCH | 0 | 0/5/0 | 0 → 0 |
| S-0023 | RHUBAFURAN TOCO | NEEDS_REVIEW | 6 | LIKELY_MATCH | 0 | 0/7/0 | 20 → 20 |
| S-0020 | ALD C-11 INTRELEVEN (TT) PRG | NEEDS_REVIEW | 7 | LIKELY_MATCH | 2 | 0/6/2 | 0 → 0 |
| S-0508 | AMBROCEMOR EXT | NO_PUBLIC_DATA_FOUND | 0 | — | 0 | 0/1/0 | 0 → 0 |

## Limitaciones reales del entorno y alternativas

- **Buscadores web**: no utilizables por script (robots.txt de Google/Bing prohíbe /search; DuckDuckGo cortado por el proxy; sin clave de API). Las búsquedas las hizo el agente operador con su herramienta de búsqueda y quedaron registradas tal cual (`data/search_ingest/`). Alternativa para escalar: una API de búsqueda con clave (Brave Search API, SerpAPI) escribiendo el mismo formato.
- **IFF (iff.com, incluido el compendio LMR) y dsm-firmenich Studio** responden 403 a cualquier acceso automatizado; **Givaudan** sirvió CAPTCHA tras varias peticiones; **TGSC y ScenTree** prohíben explícitamente a los agentes de Anthropic en robots.txt. Todo ello quedó como MANUAL_RETRIEVAL_REQUIRED. Alternativa: descargar a mano (navegador) las fichas/PDF listados en cada material y dejarlos en una carpeta; el pipeline puede procesar archivos locales con la misma extracción y trazabilidad.
- **PubChem** limitó la tasa de peticiones (429/503) durante el piloto; el pipeline se detuvo (cortacircuitos) y dejó esas consultas pendientes de reanudar.
- La composición GC-MS publicada es siempre REFERENCE_COMPOSITION de muestras de investigación, nunca la botella ISIPCA.
- Nada se ha escrito en el master. Aplicar cambios requiere una fase explícita de aprobación.

## Detalle por material

## S-0002 — VERBENAL

*Grupo piloto:* IFF_SYNTHETIC · *Qué prueba:* exact identity, IFF domain blocked -> distributor fallback, dose missing (Tier A but NOT_READY)
*Estado final:* **NO_PUBLIC_DATA_FOUND** — no usable public data in this targeted pass (not exhaustive)
*Master antes:* tier `A_EXACT_COMMERCIAL_GRADE`, CAS `55722-59-3`, readiness 33 (NOT_READY)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 33 (NOT_READY); si se aprueban también los NEEDS_REVIEW → 33 (NOT_READY)

**Queries realizadas**

- `claude_websearch` · Verbenal IFF → 9 resultados
- `claude_websearch` · Verbenal CAS 55722-59-3 → 10 resultados
- `claude_websearch` · Verbenal safety data sheet → 9 resultados
- `claude_websearch` · Verbenal use level → 9 resultados
- `claude_websearch` · Verbenal IFF pdf → 9 resultados
- `claude_websearch` · Verbenal odor vapor pressure → 9 resultados
- `claude_websearch` · Verbenal perfumersworld → 9 resultados
- `pubchem_api` · cas:55722-59-3 → 0 resultados

**Fuentes encontradas:** 58 URLs distintas; 13 seleccionadas para descarga (MANUAL_RETRIEVAL_REQUIRED: 4, ROBOTS_DISALLOWED: 1, FETCHED: 8); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://www.iff.com/scent/ingredients-compendium/verbenal/ — MANUAL_RETRIEVAL_REQUIRED (HTTP 403 (site refuses automated access; not bypassed))
- https://www.specialchem.com/cosmetics/product/iff-verbenal — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.chemicalbook.com/msds/verbenone.htm — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 429 (site refuses automated access; not bypassed))
- https://www.chemicalbook.com/msds/verbenone.pdf — MANUAL_RETRIEVAL_REQUIRED (HTTP 429 (site refuses automated access; not bypassed))
- https://www.tandfonline.com/doi/pdf/10.1080/00022470.1974.10470005 — MANUAL_RETRIEVAL_REQUIRED (HTTP 403 (site refuses automated access; not bypassed))

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| EXACT_CAS_ONLY | SECONDARY_DB | UNKNOWN_LICENSE | [55722-59-3 / CAS DataBase](https://m.chemicalbook.com/CASEN_55722-59-3.htm) | CAS match ['55722-59-3'] |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [Verbenalinosides A and B, Two Iridoid–Phenylethanoid Glycoside Conjug…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=11904641&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)
- [Verbena officinalis L. Herb Extract, Its Amino Acid Preparations and …](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=12429985&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)
- [Trends in odor intensity for human and electronic noses: Relative rol…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=20396&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)
- [In Vitro Human Metabolism and Inhibition Potency of Verbascoside for …](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=6600574&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)
- [Anticonvulsant, Anxiolytic, and Sedative Activities of Verbena offici…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=5174135&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)
- [Two New Iridoids from Verbena officinalis L](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=6271327&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)

**Fuentes rechazadas:** 7

- Verbena Oil | — neither trade name nor CAS found
- Veratryl Aldehyde (Powder) | — neither trade name nor CAS found
- Odor vapor pressure and quality modulate local field potential oscill… — neither trade name nor CAS found
- (-)-Verbenone SDS｜MSDS — labelled CAS ['1196-01-6'] not in master set ['55722-59-3']; neither trade name nor CAS found
- Page 1 of 6 — neither trade name nor CAS found
- Page 1 ( 10 ) — neither trade name nor CAS found
- Verbenalin - Wikipedia — labelled CAS ['548-37-8'] not in master set ['55722-59-3']; neither trade name nor CAS found

**Confianza de identidad:** EXACT_CAS_ONLY (score 0.60)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 55722-59-3 |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| logp | 2.867 (est) | 2.867 log10 | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| density | 0.856±0.06 g/cm3(Predicted) | 0.856 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| boiling_point | 220.2±9.0 °C(Predicted) | 220.2 C | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| ec_number | 259-777-1 |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| gcms_study | Verbenalinosides A and B, Two Iridoid–Phenylethanoid Glycoside Conjug… |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| gcms_study | Verbena officinalis L. Herb Extract, Its Amino Acid Preparations and … |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| gcms_study | Trends in odor intensity for human and electronic noses: Relative rol… |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| gcms_study | In Vitro Human Metabolism and Inhibition Potency of Verbascoside for … |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| gcms_study | Anticonvulsant, Anxiolytic, and Sedative Activities of Verbena offici… |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| gcms_study | Two New Iridoids from Verbena officinalis L |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| molecular_formula | C10H16O |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| molecular_weight | 152.23 | 152.23 g/mol | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** ninguna encontrada
**SDS/CLP (por SDS, sin mezclar):** ningún SDS del producto analizado

**Cambios propuestos:** 1 (NEEDS_REVIEW: 1)

- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=SEARCHED_NO_USABLE_DATA

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/ingredients-compendium/verbenal/): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Sin SDS del producto analizable: pedir SDS al proveedor/escuela.
- 6 documento(s) de identidad ambigua esperan revisión humana.

---

## S-0468 — HEALINGWOOD

*Grupo piloto:* IFF_SYNTHETIC · *Qué prueba:* exact identity, Tier A NOT_READY, SDS
*Estado final:* **NO_PUBLIC_DATA_FOUND** — no usable public data in this targeted pass (not exhaustive)
*Master antes:* tier `A_EXACT_COMMERCIAL_GRADE`, CAS `5986-55-0`, readiness 40 (NOT_READY)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 40 (NOT_READY); si se aprueban también los NEEDS_REVIEW → 40 (NOT_READY)

**Queries realizadas**

- `claude_websearch` · Healingwood IFF → 10 resultados
- `claude_websearch` · Healingwood CAS → 10 resultados
- `claude_websearch` · Healingwood safety data sheet → 9 resultados
- `claude_websearch` · Healingwood use level fragrance → 9 resultados
- `claude_websearch` · Healingwood IFF pdf → 9 resultados
- `claude_websearch` · Healingwood odor patchouli vapor pressure → 9 resultados
- `claude_websearch` · Healingwood patchoulol biotech IFF 5986-55-0 → 10 resultados
- `claude_websearch` · Healingwood perfumersworld → 10 resultados
- `pubchem_api` · cas:5986-55-0 → 0 resultados

**Fuentes encontradas:** 47 URLs distintas; 19 seleccionadas para descarga (ROBOTS_DISALLOWED: 5, MANUAL_RETRIEVAL_REQUIRED: 1, FETCHED: 13); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://basenotes.com/threads/healingwood-iff-what-is-it-exactly-edit-its-natural-patchoulol-please-delete.532151/ — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://basenotes.com/threads/healingwood-iff-what-is-it-exactly-edit-its-natural-patchoulol.532151/ — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.fragrantica.com/notes/Healingwood-1526.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /notes/Healingwood-1526.html -> MANUAL_RETRIEVAL_REQUI…)
- https://www.iff.com/scent/lmr-compendium/healingwood/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- http://lmrnaturals.iff.com/en/scent/lmr-naturals/online-compendium/healingwood — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.firmenich.com/sites/default/files/uploads/files/ingredients/marketing-sheet/perfumery/CLEARWOOD_970953.pdf — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Patchouli alcohol CAS# 5986-55-0: Odor profile, Molecular p…](https://scent.vn/en/pages/compound/patchouli-alcohol-1394) | trade/common name in text: 'healingwood'; CAS match ['5986-55-0'] |
| EXACT_CAS_ONLY | SECONDARY_DB | UNKNOWN_LICENSE | [5986-55-0 / CAS DataBase](https://m.chemicalbook.com/CASEN_5986-55-0.htm) | CAS match ['5986-55-0'] |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [Characterization of Bioactive Compounds from Patchouli Extracted via …](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=9503852&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)

**Fuentes rechazadas:** 11

- https://www.knowde.com/stores/srs-aromatics/products/srs-aromatics-he… — trade/common name in title: 'healingwood'; neither trade name nor CAS found
- Clearwood | — neither trade name nor CAS found
- W-Wood Fleuressence | — neither trade name nor CAS found
- Product Page — neither trade name nor CAS found; NO_CONTENT: only site template after removing 215 shared lines (page likely…
- SAFETY DATA SHEET — neither trade name nor CAS found
- GHS Safety Data Sheet - US — neither trade name nor CAS found; SDS issued by dsm-firmenich (section 1), hosted by a third party
- SAFETY DATA SHEET — neither trade name nor CAS found
- Safety Data Sheet — neither trade name nor CAS found
- Page 1 ( 13 ) — neither trade name nor CAS found
- Safety data sheet - Wikipedia — neither trade name nor CAS found
- Safety Data Sheet — neither trade name nor CAS found

**Confianza de identidad:** LIKELY_MATCH (score 0.65)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 5986-55-0 |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| vapour_pressure | 0.14Pa at 24℃ | 0.14 Pa | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| logp | 5.5 at 25℃ | 5.5 log10 | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| density | d420 1.0284 | 1.0284 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| refractive_index | nD65 1.5029 | 1.5029 nD | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| boiling_point | bp8 140° | 140.0 C | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| physical_state | Solid |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| solubility | Chloroform (Sparingly), Methanol (Slightly) |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| solubility | 41.8mg/L at 24℃ |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| odour_description | at 100.00 %. patchouli earthy camphor powdery |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| ec_number | 227-807-2 |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| gcms_study | Characterization of Bioactive Compounds from Patchouli Extracted via … |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| molecular_formula | C15H26O |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |
| molecular_weight | 222.37 | 222.37 g/mol | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | m.chemicalbook.com |

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** vapour_pressure=0.14Pa at 24℃ (SECONDARY_REFERENCE, NEEDS_REVIEW)
**SDS/CLP (por SDS, sin mezclar):** ningún SDS del producto analizado

**Cambios propuestos:** 1 (NEEDS_REVIEW: 1)

- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=SEARCHED_NO_USABLE_DATA

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/lmr-compendium/healingwood/): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Sin SDS del producto analizable: pedir SDS al proveedor/escuela.
- 1 documento(s) de identidad ambigua esperan revisión humana.

---

## S-0486 — BACDANOL TOCO

*Grupo piloto:* IFF_SYNTHETIC · *Qué prueba:* exact identity, shared CAS with SANJINOL (S-0493) -> identity by grade not CAS
*Estado final:* **NEEDS_REVIEW** — 2 conflicts; 14 changes need review
*Master antes:* tier `A_EXACT_COMMERCIAL_GRADE`, CAS `28219-61-6`, readiness 61 (PARTIAL)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 61 (PARTIAL); si se aprueban también los NEEDS_REVIEW → 61 (PARTIAL)

**Queries realizadas**

- `claude_websearch` · Bacdanol IFF → 10 resultados
- `claude_websearch` · Bacdanol CAS 28219-61-6 → 9 resultados
- `claude_websearch` · Bacdanol safety data sheet → 9 resultados
- `claude_websearch` · Bacdanol use level → 9 resultados
- `claude_websearch` · Bacdanol IFF pdf → 10 resultados
- `claude_websearch` · Bacdanol odor vapor pressure → 10 resultados
- `claude_websearch` · Bacdanol Vigon → 9 resultados
- `claude_websearch` · Bacdanol TOCO tocopherol IFF → 10 resultados
- `pubchem_api` · cas:28219-61-6 → 0 resultados

**Fuentes encontradas:** 51 URLs distintas; 17 seleccionadas para descarga (FETCHED: 14, ROBOTS_DISALLOWED: 2, MANUAL_RETRIEVAL_REQUIRED: 1); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://cosmetics.specialchem.com/product/i-iff-bacdanol — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.iff.com/scent/ingredients-compendium/bacdanol/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.specialchem.com/cosmetics/product/iff-bacdanol — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Bacdanol (IFF)](https://www.hekserij.nl/wp-content/uploads/2024/10/SDS-23144-Bacdanol-IFF-2024-05.pdf) | trade/common name in title: 'bacdanol'; CAS match ['28219-61-6']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [SAFETY DATA SHEET](https://shop.perfumersapprentice.com/msds/9237.pdf) | trade/common name in text: 'bacdanol'; CAS match ['28219-61-6']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party; SDS issued by IFF… |
| EXACT_NAME_MANUFACTURER | DISTRIBUTOR | UNKNOWN_LICENSE | [BACDANOL® IFF](https://www.ventos.com/index.php/en/producto/2007/BACDANOL+IFF/BACDANOL%C2%AE++IFF) | trade/common name in title: 'bacdanol'; CAS match ['28219-61-6']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Perfumers Apprentice - Bacdanol **](https://shop.perfumersapprentice.com/p-9237-bacdanol.aspx) | trade/common name in title: 'bacdanol'; CAS match ['28219-61-6']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Bacdanol (28219-61-6) — Synthetic Ingredient for Perfumery …](https://www.scentspiracy.com/fragrance-ingredients/p/bacdanol) | trade/common name in title: 'bacdanol'; CAS match ['28219-61-6']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Bacdanol from IFF-Aromatic Chemicals – Bulkaroma](https://bulkaroma.com/products/bacdanol-iff) | trade/common name in title: 'bacdanol'; CAS match ['28219-61-6']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Bacdanol® – Fraterworks](https://fraterworks.com/products/bacdanol) | trade/common name in title: 'bacdanol'; CAS match ['28219-61-6']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Bacdanol - IFF – Global Perfumes Shop](https://globalperfumesshop.com/products/bacdanol-iff) | trade/common name in title: 'bacdanol'; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Safety Data Sheet](https://media.knowde.com/image/upload/v1731934339/10341-01Bacdanol_SDSEUEN.pdf20241118-1-8n7ky9.pdf) | trade/common name in text: 'bacdanol'; CAS match ['28219-61-6'] |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Sanderol RH (Bacdanol) - Vigon](https://www.vigon.com/product/sanderol-rh-bacdanol/) | trade/common name in title: 'bacdanol' |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Bacdanol /](https://www.perfumersworld.com/view.php?pro_id=4WR00045) | trade/common name in title: 'bacdanol'; CAS match ['28219-61-6'] |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Bacdanol](https://www.chemtexusa.com/wp-content/uploads/2021/03/B1000_Bacdanol.pdf) | trade/common name in title: 'bacdanol'; CAS match ['28219-61-6'] |

**Fuentes rechazadas:** 2

- https://www.vigon.com/docgen?type=ifra_statement&data=503492 — neither trade name nor CAS found; NO_CONTENT: only site template after removing 216 shared lines (page likely…
- IFRA — trade/common name in title: 'bacdanol'; neither trade name nor CAS found

**Confianza de identidad:** EXACT_NAME_MANUFACTURER (score 0.80)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 28219-61-6 |  | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| cas | 28219-61-6 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | VALID | shop.perfumersapprentice.com |
| cas | 28219-61-6 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| cas | 28219-61-6 |  | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| use_level | 0.5-5% | 0.5–5.0 % | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | www.scentspiracy.com |
| use_level | 0.5-2% | 0.5–2.0 % | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| vapour_pressure | 0.000017 kPa 20 | 0.017 Pa | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | media.knowde.com |
| vapour_pressure | < 0.01 hPa | 1.0 Pa | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | VALID | shop.perfumersapprentice.com |
| vapour_pressure | 0.01 hPa | 1.0 Pa | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | VALID | shop.perfumersapprentice.com |
| vapour_pressure | < 0.0002 hPa | 0.02 Pa | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| vapour_pressure | 0.0002 hPa | 0.02 Pa | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| logp | 4.4 | 4.4 log10 | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | media.knowde.com |
| logp | 4.54 | 4.54 log10 | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| logp | 6 | 6.0 log10 | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| logp | n- : log Pow: 4.540 | 4.54 log10 | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | VALID | shop.perfumersapprentice.com |
| logp | 4.540 | 4.54 log10 | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | VALID | shop.perfumersapprentice.com |
| logp | 4.4 (Experimental value; OECD 117: Partition Coefficient (n-octanol/w… | 4.4 log10 | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| logp | 4.4 | 4.4 log10 | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| tenacity | Lasts > 336 hours on a smelling strip. | 336.0 hours | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| density | 0.913-0.917 | 0.915 g/cm3 (or SG, ~equal at 20-25 C) | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | media.knowde.com |
| density | 0.92 | 0.92 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| flash_point | 140 C | 140.0 C | DISTRIBUTOR_SDS | LIKELY_MATCH | CONFLICT | media.knowde.com |
| flash_point | 110°C | 110.0 C | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | CONFLICT | www.hekserij.nl |
| flash_point | 110 C | 110.0 C | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | CONFLICT | www.hekserij.nl |
| flash_point | > 94 °C | 94.0 C | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | CONFLICT | shop.perfumersapprentice.com |
| flash_point | >94 C | 94.0 C | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | CONFLICT | shop.perfumersapprentice.com |
| flash_point | 212°F (94°C) | 100.0 C | DISTRIBUTOR_SPEC | LIKELY_MATCH | CONFLICT | www.vigon.com |
| flash_point | 140 °C | 140.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | www.chemtexusa.com |
| flash_point | 140 C | 140.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | www.chemtexusa.com |
| flash_point | 94 C | 94.0 C | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | CONFLICT | shop.perfumersapprentice.com |
| boiling_point | 279 C | 279.0 C | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | media.knowde.com |
| boiling_point | 279°C | 279.0 C | DISTRIBUTOR_SPEC | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| boiling_point | 279 °C | 279.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| boiling_point | 279 C | 279.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| physical_state | liquid |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | VALID | shop.perfumersapprentice.com |
| physical_state | Liquid |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| physical_state | Liquid. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| physical_state | Colourless liquid |  | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| solubility | Notavailable |  | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| solubility | Insoluble in water. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| odour_description | Notavailable |  | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| product_code | B1000 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| botanical_name | ETHYL TRIMETHYLCYCLOPENTENE BUTENOL |  | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| clp_class | Skin Irrit. 2 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| clp_class | Eye Irrit. 2A |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| clp_class | Aquatic Acute 1 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| clp_class | Aquatic Chronic 1 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| h_statement | H315 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | media.knowde.com |
| h_statement | H319 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | media.knowde.com |
| h_statement | H411 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | media.knowde.com |
| h_statement | H315 |  | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| h_statement | H319 |  | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| h_statement | H411 |  | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| h_statement | EUH208 |  | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| h_statement | H319 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | VALID | shop.perfumersapprentice.com |
| h_statement | H410 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | VALID | shop.perfumersapprentice.com |
| h_statement | H315 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| h_statement | H319 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| h_statement | H400 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| h_statement | H410 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
_… 15 claims más en data/staging.sqlite_

**Evidencia de dosis:** 0.5-5% (RETAILER (SECONDARY CLAIM), www.scentspiracy.com, VALID); 0.5-2% (RETAILER (SECONDARY CLAIM), fraterworks.com, VALID)
**Evidencia de performance:** vapour_pressure=0.000017 kPa 20 (DISTRIBUTOR_SDS, NEEDS_REVIEW); vapour_pressure=< 0.01 hPa (MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF), VALID); vapour_pressure=0.01 hPa (MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF), VALID); vapour_pressure=< 0.0002 hPa (SECONDARY_REFERENCE SDS, NEEDS_REVIEW); vapour_pressure=0.0002 hPa (SECONDARY_REFERENCE SDS, NEEDS_REVIEW); tenacity=Lasts > 336 hours on a smelli… (RETAILER (SECONDARY CLAIM), VALID)
**SDS/CLP (por SDS, sin mezclar):** media.knowde.com: H315, H319, H411, Warning · shop.perfumersapprentice.com: H319, H410, Warning · www.chemtexusa.com: Aquatic Acute 1, Aquatic Chronic 1, Eye Irrit. 2A, H315, H319, H400, H410, Skin Irrit. 2 · www.hekserij.nl: EUH208, H315, H319, H411

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6) — valores: 140 C [DISTRIBUTOR]; 110°C [RETAILER]; 110 C [RETAILER]; > 94 °C [RETAILER]; >94 C [RETAILER]; 212°F (94°C) [DISTRIBUTOR]; 140 °C [SECONDARY]; 140 C [SECONDARY]
- `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] — valores: H315 [DISTRIBUTOR]; H319 [DISTRIBUTOR]; H411 [DISTRIBUTOR]; H315 [RETAILER]; H319 [RETAILER]; H411 [RETAILER]; EUH208 [RETAILER]; H319 [RETAILER]

**Cambios propuestos:** 15 (NEEDS_REVIEW: 13, BLOCKED_CONFLICT: 2)

- `NEEDS_REVIEW` · DOSE EVIDENCE STRUCTURED · APPEND_ROW · dose_type=SECONDARY_REFERENCE_MAX_USE, value_text=0.5-5%, unit=%
- `NEEDS_REVIEW` · DOSE EVIDENCE STRUCTURED · APPEND_ROW · dose_type=SECONDARY_REFERENCE_MAX_USE, value_text=0.5-2%, unit=%
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=vapor_pressure_supplier, value=0.017, unit=Pa (converted from 0.000017 kpa (temperature not stated))
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=logP_supplier, value=4.4, unit=log10
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=density_20C, value=0.915, unit=g/cm3 (or SG, ~equal at 20-25 C)
- `BLOCKED_CONFLICT` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=140.0, unit=C
- `BLOCKED_CONFLICT` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=100.0, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=boiling_point_normal, value=279.0, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=boiling_point_normal, value=279.0, unit=C
- `NEEDS_REVIEW` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=>336.0, unit=hours
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H315, H319, H411
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: EUH208, H315, H319, H411
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H319, H410
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes=Aquatic Acute 1; Aquatic Chronic 1; Eye Irrit. 2A; Skin Irrit. 2 | H: H315, H319, H400, H410
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/ingredients-compendium/bacdanol/): recuperar manualmente y re-ejecutar la extracción.
- Resolver conflicto en `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6)
- Resolver conflicto en `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only]

---

## S-0526 — MUSCEMOR (ELINCS)

*Grupo piloto:* IFF_SYNTHETIC · *Qué prueba:* multi-CAS captive, PDF/SDS
*Estado final:* **NEEDS_REVIEW** — 1 conflicts; 3 changes need review
*Master antes:* tier `A_EXACT_COMMERCIAL_GRADE`, CAS `82356-51-2 | 63314-79-4`, readiness 49 (PARTIAL)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 49 (PARTIAL); si se aprueban también los NEEDS_REVIEW → 49 (PARTIAL)

**Queries realizadas**

- `claude_websearch` · Muscemor IFF → 10 resultados
- `claude_websearch` · Muscemor CAS 82356-51-2 → 10 resultados
- `claude_websearch` · Muscemor safety data sheet → 9 resultados
- `claude_websearch` · Muscemor use level → 9 resultados
- `claude_websearch` · Muscemor IFF pdf → 9 resultados
- `claude_websearch` · Muscemor odor vapor pressure → 9 resultados
- `claude_websearch` · Muscemor 63314-79-4 → 10 resultados
- `claude_websearch` · Muscemor perfumersworld → 10 resultados
- `pubchem_api` · cas:82356-51-2 → 0 resultados
- `pubchem_api` · cas:63314-79-4 → 0 resultados

**Fuentes encontradas:** 52 URLs distintas; 25 seleccionadas para descarga (FETCHED: 13, ROBOTS_DISALLOWED: 8, MANUAL_RETRIEVAL_REQUIRED: 1, ENV_UNREACHABLE: 3); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://cosmetics.specialchem.com/product/i-iff-muscemor — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.iff.com/scent/ingredients-compendium/muscemor/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- http://lmrnaturals.iff.com/en/scent/fragrance-ingredients/online-compendium-new/muscemor — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://lmrnaturals.iff.com/en/site-services/fragrance-online-compendium/muscemor — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: ('Connection aborted.', Connec…)
- https://www.specialchem.com/cosmetics/product/iff-muscor — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.scentree.co/en/Muscenone%C2%AE.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /en/Muscenone%C2%AE.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://datasheets.scbt.com/sc-200460.pdf — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.fishersci.com/store/msds?partNumber=AC218120050&productDescription=MUSCIMOL+HYDRATE%2C+98+%25+5MG&vendorId=VN00032119&countryCode=US&language=en — ENV_UNREACHABLE (robots.txt unreachable: HTTPSConnectionPool(host='www.fishersci.com', port=443): Read tim…)
- https://pim-resources.coleparmer.com/sds/00478.pdf — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.t3db.ca/system/msds/attachments/000/002/038/original/T3D2456.pdf — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.specialchem.com/cosmetics/product/iff-muscemor — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://pellwall.com/products/muscenone — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: HTTPSConnectionPool(host='pell…)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| EXACT_NAME_MANUFACTURER | DISTRIBUTOR | UNKNOWN_LICENSE | [MUSCEMOR IFF](https://www.ventos.com/index.php/en/producto/9969) | trade/common name in title: 'muscemor'; CAS match ['63314-79-4', '82356-51-2']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | DISTRIBUTOR | UNKNOWN_LICENSE | [MUSCEMOR IFF](https://www.ventos.com/index.php/en/producto/9969/MUSCEMOR+IFF/223) | trade/common name in title: 'muscemor'; CAS match ['63314-79-4', '82356-51-2']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | DISTRIBUTOR | UNKNOWN_LICENSE | [L E A D E R S I N E S S E N C E](https://www.ventos.com/index.php/en/?option=com_evsa&task=documentacion.mostrar&codi=001_RZQUZPJGX0_9969) | trade/common name in text: 'muscemor'; CAS match ['63314-79-4', '82356-51-2']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | SECONDARY | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://finefrag.com/wp-content/uploads/2020/06/MUSCEMOR-MSDS.pdf) | trade/common name in title: 'muscemor'; CAS match ['63314-79-4']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [L E A D E R S I N E S S E N C E](https://www.ventos.com/index.php/en/?option=com_evsa&task=documentacion.mostrar&codi=001_E1XBSERFOL_16419) | trade/common name in text: 'muscemor'; CAS match ['63314-79-4', '82356-51-2'] |
| EXACT_CAS_ONLY | RETAILER | RESEARCH_ONLY | [Muscenone (CAS 82356-51-2 / 63314-79-4 / 36399-15-2) – Synt…](https://www.scentspiracy.com/fragrance-ingredients/p/muscenone) | CAS match ['63314-79-4', '82356-51-2']; expected manufacturer 'IFF' mentioned |
| EXACT_CAS_ONLY | SECONDARY | UNKNOWN_LICENSE | [muscenone (Cas 82356-51-2) – Parchem](http://www.parchem.com/chemical-supplier-distributor/muscenone-015144.aspx) | CAS match ['82356-51-2'] |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [Trends in odor intensity for human and electronic noses: Relative rol…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=20396&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)
- [Muscenone® – Fraterworks](https://fraterworks.com/products/muscenone) — trade/common name in text: 'muscemor'; CAS match ['82356-51-2']; page is about another trade product ('Muscenone'); same CAS/name mention but a different comme…
- [Muscenone® Delta from dsm-firmenich-Aromatic Chemicals – Bulkaroma](https://bulkaroma.com/en-us/products/muscenone-delta-firmenich) — trade/common name in text: 'muscemor'; CAS match ['63314-79-4']; expected manufacturer 'IFF' mentioned; page is about another trade product ('Muscenone'); same…

**Fuentes rechazadas:** 4

- Muscone | — neither trade name nor CAS found
- Odor vapor pressure and quality modulate local field potential oscill… — neither trade name nor CAS found
- SAFETY DATA SHEET — neither trade name nor CAS found
- Muscimol SDS, 2763-96-4 Safety Data Sheets - ECHEMI — neither trade name nor CAS found

**Confianza de identidad:** EXACT_NAME_MANUFACTURER (score 0.80)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 63314-79-4 |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| cas | 82356-51-2 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| cas | 82356-51-2 |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | www.parchem.com |
| use_level | 1-5% | 1.0–5.0 % | RETAILER (SECONDARY CLAIM) | EXACT_CAS_ONLY | VALID | www.scentspiracy.com |
| use_level | up to 5% | None–5.0 % | RETAILER (SECONDARY CLAIM) | EXACT_CAS_ONLY | VALID | www.scentspiracy.com |
| use_level | 0.5-5% | 0.5–5.0 % | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| vapour_pressure | < 0,01 hPa | 1.0 Pa | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| vapour_pressure | 0,01 hPa | 1.0 Pa | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| logp | : log Pow: 6,060 | 6.06 log10 | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| logp | 6,060 | 6.06 log10 | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| tenacity | Lasts > 400 hours on a smelling strip. | 400.0 hours | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| density | 0.923-0.933 g/ml at 20°C | 0.928 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | CONFLICT | finefrag.com |
| density | 0.923-0.933 | 0.928 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | CONFLICT | finefrag.com |
| density | 0.856 0.06 gcm3 | 0.856 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE | EXACT_CAS_ONLY | CONFLICT | www.parchem.com |
| density | 0.925 - 0.935 | 0.93 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE | EXACT_CAS_ONLY | CONFLICT | www.parchem.com |
| refractive_index | 1.486 - 1.490 | 1.488 nD | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | www.parchem.com |
| flash_point | 100 °C | 100.0 C | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| flash_point | 100 C | 100.0 C | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| flash_point | >100°C CC | 100.0 C | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | www.parchem.com |
| physical_state | liquid |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| physical_state | Colourless liquid |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| solubility | ethanol |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | www.parchem.com |
| odour_description | Animalic |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| odour_description | musk odor |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | www.parchem.com |
| product_code | 4299 - IFF IPC: 131730 |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| ec_number | 429-900-5 |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| botanical_name | METHYL CYCLOPENTADECENONE |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| iso_standard | ISO 9001:2015 |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | www.parchem.com |
| h_statement | H317 |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| h_statement | H400 |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| h_statement | H410 |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| signal_word | Warning |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| sds_product_name | Product name: MUSCEMOR |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| sds_component_cas | 63314-79-4 |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| stability_text | Stable under normal conditions. |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| gcms_study | Trends in odor intensity for human and electronic noses: Relative rol… |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| molecular_formula | C H O |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| molecular_formula | C 1 6 H 2 8 O |  | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | www.parchem.com |
| molecular_weight | 236 g/mol | 236.0 g/mol | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| molecular_weight | 236.39 | 236.39 g/mol | SECONDARY_REFERENCE | EXACT_CAS_ONLY | NEEDS_REVIEW | www.parchem.com |

**Evidencia de dosis:** 1-5% (RETAILER (SECONDARY CLAIM), www.scentspiracy.com, VALID); up to 5% (RETAILER (SECONDARY CLAIM), www.scentspiracy.com, VALID); 0.5-5% (RETAILER (SECONDARY CLAIM), fraterworks.com, NEEDS_REVIEW)
**Evidencia de performance:** vapour_pressure=< 0,01 hPa (SECONDARY_REFERENCE SDS, NEEDS_REVIEW); vapour_pressure=0,01 hPa (SECONDARY_REFERENCE SDS, NEEDS_REVIEW); tenacity=Lasts > 400 hours on a smelli… (RETAILER (SECONDARY CLAIM), NEEDS_REVIEW)
**SDS/CLP (por SDS, sin mezclar):** finefrag.com: H317, H400, H410, Warning

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `density`: density: independent sources disagree beyond tolerance ('abs', 0.012) — valores: 0.923-0.933 g/ml at 20°C [SECONDARY]; 0.923-0.933 [SECONDARY]; 0.856 0.06 gcm3 [SECONDARY]; 0.925 - 0.935 [SECONDARY]

**Cambios propuestos:** 4 (NEEDS_REVIEW: 4)

- `NEEDS_REVIEW` · DOSE EVIDENCE STRUCTURED · APPEND_ROW · dose_type=SECONDARY_REFERENCE_MAX_USE, value_text=1-5%, unit=%
- `NEEDS_REVIEW` · DOSE EVIDENCE STRUCTURED · APPEND_ROW · dose_type=SECONDARY_REFERENCE_MAX_USE, value_text=0.5-5%, unit=%
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H317, H400, H410
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/ingredients-compendium/muscemor/): recuperar manualmente y re-ejecutar la extracción.
- Resolver conflicto en `density`: density: independent sources disagree beyond tolerance ('abs', 0.012)
- 3 documento(s) de identidad ambigua esperan revisión humana.

---

## S-0479 — ISO E SUPER TOCO

*Grupo piloto:* IFF_SYNTHETIC · *Qué prueba:* well documented, multiple CAS -> conflict detection, dose already in master -> duplicate detection
*Estado final:* **NEEDS_REVIEW** — 2 conflicts; 9 changes need review
*Master antes:* tier `A_EXACT_COMMERCIAL_GRADE`, CAS `54464-57-2 | 68155-66-8 | 68155-67-9`, readiness 89 (READY_WITH_CAVEATS)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 89 (READY_WITH_CAVEATS); si se aprueban también los NEEDS_REVIEW → 89 (READY_WITH_CAVEATS)

**Queries realizadas**

- `claude_websearch` · Iso E Super IFF → 10 resultados
- `claude_websearch` · Iso E Super CAS 54464-57-2 68155-66-8 68155-67-9 → 10 resultados
- `claude_websearch` · Iso E Super safety data sheet → 9 resultados
- `claude_websearch` · Iso E Super use level → 9 resultados
- `claude_websearch` · Iso E Super IFF pdf → 9 resultados
- `claude_websearch` · Iso E Super odor vapor pressure → 9 resultados
- `claude_websearch` · Iso E Super TOCO tocopherol IFF → 9 resultados
- `claude_websearch` · Iso E Super Ventos → 9 resultados
- `pubchem_api` · cas:54464-57-2 → 0 resultados
- `pubchem_api` · cas:68155-66-8 → 0 resultados
- `pubchem_api` · cas:68155-67-9 → 0 resultados

**Fuentes encontradas:** 49 URLs distintas; 22 seleccionadas para descarga (ROBOTS_DISALLOWED: 5, FETCHED: 14, MANUAL_RETRIEVAL_REQUIRED: 1, HTTP_ERROR: 1, ENV_UNREACHABLE: 1); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://cosmetics.specialchem.com/product/i-iff-iso-e-super — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.iff.com/scent/ingredients-compendium/iso-e-super/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://datasheets.scbt.com/sc-211663.pdf — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.scribd.com/document/710633645/Iso-E-Super-SDS — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /document/710633645/Iso-E-Super-SDS -> MANUAL_RETRIEVA…)
- https://www.scribd.com/document/849766351/Ghs-Iso-e-Super-Msds — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /document/849766351/Ghs-Iso-e-Super-Msds -> MANUAL_RET…)
- http://lmrnaturals.iff.com/en/scent/fragrance-ingredients/online-compendium-new/iso-e-super-tocopherol — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: ('Connection aborted.', Connec…)
- https://www.specialchem.com/cosmetics/product/iff-iso-e-super-tocopherol — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Iso E Super (IFF)](https://www.hekserij.nl/wp-content/uploads/2025/03/SDS-23021-Iso-E-Super-IFF-2025-03.pdf) | trade/common name in title: 'iso e super'; CAS match ['68155-66-8']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | DISTRIBUTOR | UNKNOWN_LICENSE | [ISO E SUPER® IFF](https://www.ventos.com/index.php/en/producto/3075/ISO%20E%20SUPER%20IFF/ISO%20E%20SUPER%C2%AE%20IFF) | trade/common name in title: 'iso e super'; CAS match ['54464-57-2', '68155-66-8']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | DISTRIBUTOR | UNKNOWN_LICENSE | [ISO E SUPER® IFF](https://www.ventos.com/index.php/en/producto/3075) | trade/common name in title: 'iso e super'; CAS match ['54464-57-2', '68155-66-8']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | SECONDARY | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://perfumersupplyhouse.com/wp-content/uploads/2019/06/ISO-E-SUPER-GHS-SDS.pdf) | trade/common name in text: 'iso e super'; CAS match ['54464-57-2', '68155-66-8', '68155-67-9']; expected manufacturer 'IFF' mentioned; manufacturer stated by a… |
| EXACT_NAME_MANUFACTURER | SECONDARY | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://finefrag.com/wp-content/uploads/2019/11/ISO-E-SUPER_00098663_GHS_MSDS_17SEP2019_112130.pdf) | trade/common name in text: 'iso e super'; CAS match ['54464-57-2', '68155-66-8', '68155-67-9']; expected manufacturer 'IFF' mentioned; manufacturer stated by a… |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Perfumers Apprentice - Iso E Super® (IFF) **](https://shop.perfumersapprentice.com/p-6120-iso-e-super-iff.aspx) | trade/common name in title: 'iso e super'; CAS match ['54464-57-2', '68155-66-8', '68155-67-9']; expected manufacturer 'IFF' mentioned; manufacturer stated by … |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Iso E Super™ – Fraterworks](https://fraterworks.com/products/iso-e-super) | trade/common name in title: 'iso e super'; CAS match ['54464-57-2']; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [ISO E Super - IFF – Global Perfumes Shop](https://globalperfumesshop.com/products/iso-e-super-iff) | trade/common name in title: 'iso e super'; expected manufacturer 'IFF' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Page 1 ( 4 )](https://shop.perfumersapprentice.com/Documents/IFRA-51/6120.pdf) | trade/common name in text: 'iso e super'; CAS match ['54464-57-2', '68155-66-8', '68155-67-9']; expected manufacturer 'IFF' mentioned; manufacturer stated by a… |
| EXACT_NAME_MANUFACTURER | SECONDARY | UNKNOWN_LICENSE | [Fragrance Product Information Sheet (FPIS)](https://perfumersupplyhouse.com/wp-content/uploads/2019/06/ISO-E-SUPER-TOCO_00091841_FPIS_IFRA-51.pdf) | trade/common name in text: 'iso e super'; CAS match ['54464-57-2', '68155-66-8', '68155-67-9']; expected manufacturer 'IFF' mentioned; manufacturer stated by a… |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Iso E Super](https://www.chemtexusa.com/wp-content/uploads/2021/03/I2200_IsoESuper.pdf) | trade/common name in title: 'iso e super'; CAS match ['54464-57-2'] |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [SAFETY DATA SHEET](http://www.mu-intel.com/upload/msds/20180320232644.pdf) | trade/common name in text: 'iso e super'; CAS match ['54464-57-2'] |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Introduction - NTP Technical Report on the Toxicity Studies…](https://www.ncbi.nlm.nih.gov/books/NBK552907/) | trade/common name in text: 'iso e super'; CAS match ['54464-57-2', '68155-66-8', '68155-67-9'] |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Iso E Super - BC Fragrance](https://shop.bcfragrance.com/product/iso-e-super/) | trade/common name in title: 'iso e super'; CAS match ['54464-57-2', '68155-66-8', '68155-67-9'] |

**Confianza de identidad:** EXACT_NAME_MANUFACTURER (score 0.80)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 68155-66-8 |  | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| cas | 54464-57-2 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| cas | 68155-66-8 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| cas | 54464-57-2 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| cas | 68155-67-9 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| cas | 54464-57-2 |  | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| cas | 54464-57-2 |  | SECONDARY_REFERENCE | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| cas | 68155-66-8 |  | SECONDARY_REFERENCE | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| cas | 68155-67-9 |  | SECONDARY_REFERENCE | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| vapour_pressure | 0.0027 hPa | 0.27 Pa | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| vapour_pressure | .00 hPa (0.00233 hPa) | 0.233 Pa | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| vapour_pressure | 00 hPa |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| vapour_pressure | 0 mm Hg 25 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.mu-intel.com |
| vapour_pressure | 0.00233 hPa | 0.233 Pa | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| logp | 5.65 | 5.65 log10 | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| logp | 6 | 6.0 log10 | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| logp | n-octanol/water : log Pow: 5.650 | 5.65 log10 | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| logp | 5.650 | 5.65 log10 | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| logp | n- : log Pow: 5.650 | 5.65 log10 | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| logp | 5.650 | 5.65 log10 | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| tenacity | Lasts > 172 hours on a smelling strip. | 172.0 hours | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| tenacity | > 48 hours | 48.0 hours | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | shop.bcfragrance.com |
| tenacity | >48 hours | 48.0 hours | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | shop.bcfragrance.com |
| substantivity_application | Very Good |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | shop.bcfragrance.com |
| density | 0.9611 – 0.967 | 0.964 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| density | 0.9611-0.967 | 0.964 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| density | 0.97 | 0.97 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.mu-intel.com |
| flash_point | 134 °C | 134.0 C | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| flash_point | 134 C | 134.0 C | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| flash_point | 134 °C | 134.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| flash_point | 134 C | 134.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| flash_point | 273 °F (134 °C) | 133.9 C | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| flash_point | 273 F | 133.9 C | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| flash_point | >200.0 F | 93.3 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.mu-intel.com |
| flash_point | 134 °C | 134.0 C | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| flash_point | 134 C | 134.0 C | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| flash_point | > 111°C | 111.0 C | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | shop.bcfragrance.com |
| flash_point | >111 C | 111.0 C | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | shop.bcfragrance.com |
| boiling_point | 276 °C | 276.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | www.chemtexusa.com |
| boiling_point | 276 C | 276.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | www.chemtexusa.com |
| boiling_point | 554.72 °F (290.40 °C) | 554.72 C | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | REJECTED | perfumersupplyhouse.com |
| boiling_point | 290.40 °C | 290.4 C | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | VALID_DISPUTED | finefrag.com |
| boiling_point | 290.40 C | 290.4 C | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | VALID_DISPUTED | finefrag.com |
| physical_state | Liquid |  | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| physical_state | Liquid |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| physical_state | Colorless to pale yellow liquid. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| physical_state | liquid at 68 °F (20 °C) (1,013.00 hPa (1,013 hPa)) |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| physical_state | CLEAR LIQUID |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| physical_state | liquid at 20 °C (1,013 hPa) |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| physical_state | Colourless liquid |  | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| physical_state | Colorless to pale yellow liquid |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | shop.bcfragrance.com |
| solubility | Insoluble in water. |  | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| solubility | 2,000 at 20 ºc |  | DISTRIBUTOR_SPEC | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | www.ventos.com |
| solubility | 2,000 at 20 ºc |  | DISTRIBUTOR_SPEC | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | www.ventos.com |
| solubility | 0.00268 g/l |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
| solubility | 0.00268 g/l |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | finefrag.com |
| product_code | 23021 |  | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | VALID | www.hekserij.nl |
| product_code | I2200 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| botanical_name | TETRAMETHYL ACETYLOCTAHYDRONAPHTHALENES |  | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| iso_standard | ISO 279 |  | SECONDARY_REFERENCE SDS | EXACT_NAME_MANUFACTURER | NEEDS_REVIEW | perfumersupplyhouse.com |
_… 51 claims más en data/staging.sqlite_

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** vapour_pressure=0.0027 hPa (SECONDARY_REFERENCE SDS, NEEDS_REVIEW); vapour_pressure=.00 hPa (0.00233 hPa) (SECONDARY_REFERENCE SDS, NEEDS_REVIEW); vapour_pressure=00 hPa (SECONDARY_REFERENCE SDS, NEEDS_REVIEW); vapour_pressure=0 mm Hg 25 (SECONDARY_REFERENCE SDS, NEEDS_REVIEW); vapour_pressure=0.00233 hPa (MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF), NEEDS_REVIEW); tenacity=Lasts > 172 hours on a smelli… (RETAILER (SECONDARY CLAIM), VALID); tenacity=> 48 hours (RETAILER (SECONDARY CLAIM), VALID); substantivity_application=Very Good (RETAILER (SECONDARY CLAIM), VALID); tenacity=>48 hours (RETAILER (SECONDARY CLAIM), VALID)
**SDS/CLP (por SDS, sin mezclar):** finefrag.com: H315, H317, H401, H410, Warning · perfumersupplyhouse.com: H315, H317, Warning · www.chemtexusa.com: Aquatic Acute 2, H315, H317, H401, Skin Irrit. 2, Skin Sens. 1 · www.hekserij.nl: H315, H317, H400, H410 · www.mu-intel.com: H315, H317, H401, H411, Warning

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `boiling_point`: boiling_point: independent sources disagree beyond tolerance ('abs', 8) [lower-tier dissent only] — valores: 276 °C [SECONDARY]; 276 C [SECONDARY]; 290.40 °C [SECONDARY]; 290.40 C [SECONDARY]
- `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] — valores: H315 [RETAILER]; H317 [RETAILER]; H400 [RETAILER]; H410 [RETAILER]; H315 [SECONDARY]; H317 [SECONDARY]; H401 [SECONDARY]; H315 [SECONDARY]

**Cambios propuestos:** 10 (NEEDS_REVIEW: 10)

- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=solubility, value=2,000 at 20 ºc
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=solubility, value=2,000 at 20 ºc
- `NEEDS_REVIEW` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=>172.0, unit=hours
- `NEEDS_REVIEW` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=>48.0, unit=hours
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H315, H317, H400, H410
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes=Aquatic Acute 2; Skin Irrit. 2; Skin Sens. 1 | H: H315, H317, H401
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H315, H317
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H315, H317, H401, H411
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H315, H317, H401, H410
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/ingredients-compendium/iso-e-super/): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Resolver conflicto en `boiling_point`: boiling_point: independent sources disagree beyond tolerance ('abs', 8) [lower-tier dissent only]
- Resolver conflicto en `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only]

---

## S-0024 — RHUBOFIX FIRM

*Grupo piloto:* GIV_DSMF_SYM · *Qué prueba:* Firmenich grade, studio.dsm-firmenich blocked -> distributor fallback
*Estado final:* **NEEDS_REVIEW** — 0 conflicts; 2 changes need review
*Master antes:* tier `B_EXACT_CHEMICAL_GRADE_UNCONFIRMED`, CAS `41816-03-9`, readiness 50 (PARTIAL)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 50 (PARTIAL); si se aprueban también los NEEDS_REVIEW → 50 (PARTIAL)

**Queries realizadas**

- `claude_websearch` · Rhubofix Firmenich → 9 resultados
- `claude_websearch` · Rhubofix dsm-firmenich → 9 resultados
- `claude_websearch` · Rhubofix CAS 41816-03-9 → 10 resultados
- `claude_websearch` · Rhubofix safety data sheet → 9 resultados
- `claude_websearch` · Rhubofix use level → 9 resultados
- `claude_websearch` · Rhubofix Firmenich pdf → 10 resultados
- `claude_websearch` · Rhubofix odor vapor pressure → 10 resultados
- `claude_websearch` · Rhubofix perfumersworld → 9 resultados
- `pubchem_api` · cas:41816-03-9 → 0 resultados

**Fuentes encontradas:** 39 URLs distintas; 23 seleccionadas para descarga (ROBOTS_DISALLOWED: 8, FETCHED: 14, MANUAL_RETRIEVAL_REQUIRED: 1); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://cosmetics.specialchem.com/product/i-firmenich-rhubofix — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.specialchem.com/cosmetics/product/dsm-firmenich-rhubofix — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.thegoodscentscompany.com/data/rw1028291.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/rw1028291.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://cosmetics.specialchem.com/product/i-dsm-firmenich-rhubofix — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.scentree.co/en/Rhubofix%C2%AE.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /en/Rhubofix%C2%AE.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://studio.dsm-firmenich.com/product/rhubofixr-pe-978880 — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.biosynth.com/p/RBA81603/41816-03-9-rhubofix — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.ulprospector.com/en/na/PersonalCare/Detail/31183/994828/Rhubofix — MANUAL_RETRIEVAL_REQUIRED (HTTP 403 (site refuses automated access; not bypassed))
- https://www.firmenich.com/sites/default/files/uploads/files/ingredients/marketing-sheet/perfumery/RHUBOFIX_978880.pdf — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Perfumers Apprentice - Rhubofix® (Firmenich)](https://shop.perfumersapprentice.com/p-8903-rhubofix-firmenich.aspx) | trade/common name in title: 'rhubofix'; CAS match ['41816-03-9']; expected manufacturer 'dsm-firmenich' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Rhubofix (41816-03-9) – Premium Synthetic Ingredient for Pe…](https://www.scentspiracy.com/fragrance-ingredients/p/rhubofix) | trade/common name in title: 'rhubofix'; CAS match ['41816-03-9']; expected manufacturer 'dsm-firmenich' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Rhubofix – Fraterworks](https://fraterworks.com/products/rhubofix) | trade/common name in title: 'rhubofix'; CAS match ['41816-03-9']; expected manufacturer 'dsm-firmenich' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Rhubofix® - dsm-firmenich – Bulkaroma](https://bulkaroma.com/products/rhubofix-firmenich) | trade/common name in title: 'rhubofix'; CAS match ['41816-03-9']; expected manufacturer 'dsm-firmenich' mentioned; manufacturer stated by a third party |
| LIKELY_MATCH | IDENTITY_DB | PRODUCTION_SAFE_WITH_ATTRIBUTION | [Rhubofix / C14H20O / CID 94522 - PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/94522) | trade/common name in title: 'rhubofix' |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Rhubofix / PerfumersWorld](https://www.perfumersworld.com/ifra/view-page.php?pro_id=3FL06757&ifra=defaultOpen) | trade/common name in title: 'rhubofix' |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Rhubofix /](https://www.perfumersworld.com/view.php?pro_id=3FL06757) | trade/common name in title: 'rhubofix'; CAS match ['41816-03-9'] |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [SAFETY DATA SHEET (GHS, Appendix 4) Version 6.1 (2024-08-01…](https://image.makewebeasy.net/makeweb/0/oCmFYX9sp/Document/Rhubofix_SDS.pdf?v=202405291424) | trade/common name in title: 'rhubofix'; CAS match ['41816-03-9'] |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Buy Online CAS Number 41816-03-9 - TRC - Rhubofix / LGC Sta…](https://www.lgcstandards.com/US/en/p/TRC-R414100) | trade/common name in title: 'rhubofix'; CAS match ['41816-03-9'] |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Rhubofix CAS# 41816-03-9: Odor profile, Molecular propertie…](https://scent.vn/en/pages/compound/rhubofix-94522) | trade/common name in title: 'rhubofix'; CAS match ['41816-03-9'] |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Rhubofix Manufacturer & Suppliers /ELAROMA-RFx - Elchemy](https://elchemy.com/product/rhubofix-935) | trade/common name in title: 'rhubofix' |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [PerfumersWorld](https://www.perfumersworld.com/ifra/IFRA/IFRA_3FL06757.pdf) — trade/common name in text: 'rhubofix'; name only in body text

**Fuentes rechazadas:** 2

- Noves fitxes EN — neither trade name nor CAS found; NO_CONTENT: only site template after removing 371 shared lines (page likely…
- Safety data sheet - Wikipedia — neither trade name nor CAS found

**Confianza de identidad:** EXACT_NAME_MANUFACTURER (score 0.80)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 41816-03-9 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| cas | 41816-03-9 |  | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| tenacity | Lasts > 100 hours on a smelling strip. | 100.0 hours | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| density | 1,010-1,050@20°C | 1.03 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| density | 1,010-1,050 | 1.03 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| flash_point | > 93°C | 93.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| flash_point | >93 C | 93.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| physical_state | Fluid liquid. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| physical_state | Clear liquid |  | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| solubility | Insoluble. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| solubility | Not stated. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| iso_standard | ISO 374 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| iso_standard | ISO 279:1999 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| iso_standard | ISO 280:1999 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| iso_standard | ISO 17025 |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.lgcstandards.com |
| clp_class | Acute Tox. 5 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| clp_class | Aquatic Acute 2 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| clp_class | Aquatic Chronic 2 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| h_statement | H303 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| h_statement | H401 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| h_statement | H411 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| signal_word | Warning |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| sds_product_name | Product name : Rhubofix |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |
| stability_text | stable under the recommended handling and storage conditions in secti… |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | image.makewebeasy.net |

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** tenacity=Lasts > 100 hours on a smelli… (RETAILER (SECONDARY CLAIM), VALID)
**SDS/CLP (por SDS, sin mezclar):** image.makewebeasy.net: Acute Tox. 5, Aquatic Acute 2, Aquatic Chronic 2, H303, H401, H411, Warning

**Cambios propuestos:** 3 (NEEDS_REVIEW: 3)

- `NEEDS_REVIEW` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=>100.0, unit=hours
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes=Acute Tox. 5; Aquatic Acute 2; Aquatic Chronic 2 | H: H303, H401, H411
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://studio.dsm-firmenich.com/product/rhubofixr-pe-978880): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- 1 documento(s) de identidad ambigua esperan revisión humana.

---

## S-0518 — HABANOLIDE (ELINCS)

*Grupo piloto:* GIV_DSMF_SYM · *Qué prueba:* Firmenich captive, SDS
*Estado final:* **NEEDS_REVIEW** — 1 conflicts; 6 changes need review
*Master antes:* tier `B_EXACT_CHEMICAL_GRADE_UNCONFIRMED`, CAS `111879-80-2`, readiness 60 (PARTIAL)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 60 (PARTIAL); si se aprueban también los NEEDS_REVIEW → 60 (PARTIAL)

**Queries realizadas**

- `claude_websearch` · Habanolide Firmenich → 10 resultados
- `claude_websearch` · Habanolide dsm-firmenich → 9 resultados
- `claude_websearch` · Habanolide CAS 111879-80-2 → 9 resultados
- `claude_websearch` · Habanolide safety data sheet → 9 resultados
- `claude_websearch` · Habanolide use level → 9 resultados
- `claude_websearch` · Habanolide Firmenich pdf → 10 resultados
- `claude_websearch` · Habanolide odor vapor pressure → 9 resultados
- `claude_websearch` · Habanolide Vigon → 9 resultados
- `pubchem_api` · cas:111879-80-2 → 0 resultados

**Fuentes encontradas:** 50 URLs distintas; 22 seleccionadas para descarga (ROBOTS_DISALLOWED: 5, FETCHED: 14, MANUAL_RETRIEVAL_REQUIRED: 2, UNSUPPORTED_CONTENT: 1); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://cosmetics.specialchem.com/product/i-dsm-firmenich-habanolide — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://studio.dsm-firmenich.com/product/habanolider-pe-947303 — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.specialchem.com/cosmetics/product/dsm-firmenich-habanolide — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://cosmetics.specialchem.com/product/i-firmenich-habanolide — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.firmenich.com/sites/default/files/uploads/files/ingredients/marketing-sheet/perfumery/HABANOLIDE_947303.pdf?07696c2= — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.ulprospector.com/en/asia/PersonalCare/Detail/31180/994811/Habanolide — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.ulprospector.com/en/na/Food/Detail/33550/994811/Habanolide — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| EXACT_NAME_MANUFACTURER | OFFICIAL_MANUFACTURER | UNKNOWN_LICENSE | [dsm-firmenich increases the production capacity of its icon…](https://our-company.dsm-firmenich.com/en/our-company/news/our-stories/2023/a-brand-new-facility-in-Europe-of-habanolide-facility.html) | trade/common name in title: 'habanolide'; official manufacturer domain (dsm-firmenich); expected manufacturer 'dsm-firmenich' mentioned |
| EXACT_NAME_MANUFACTURER | OFFICIAL_MANUFACTURER | UNKNOWN_LICENSE | [Increasing production capacity for perfumery ingredients in…](https://our-company.dsm-firmenich.com/en/our-company/news/our-stories/2024/increasing-production-capacity-for-perfumery-ingredients-in-europe.html) | trade/common name in text: 'habanolide'; official manufacturer domain (dsm-firmenich); expected manufacturer 'dsm-firmenich' mentioned |
| EXACT_NAME_MANUFACTURER | DISTRIBUTOR | UNKNOWN_LICENSE | [Habanolide /](https://www.perfumersworld.com/view.php?pro_id=3XA09821) | trade/common name in title: 'habanolide'; CAS match ['111879-80-2']; expected manufacturer 'dsm-firmenich' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Perfumers Apprentice - Habanolide® (Firmenich)](https://shop.perfumersapprentice.com/p-6099-habanolide-firmenich.aspx) | trade/common name in title: 'habanolide'; CAS match ['111879-80-2']; expected manufacturer 'dsm-firmenich' mentioned; manufacturer stated by a third party |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://www.vigon.com/product/habanolide/?doc=MSDS%2F502795_vigon_sds_us_english.pdf&namee=HabanolideSDS) | trade/common name in title: 'habanolide'; CAS match ['111879-80-2'] |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [SAFETY DATA SHEET](https://shop.perfumersapprentice.com/Images/HabanolideSDS.pdf) | trade/common name in text: 'habanolide'; CAS match ['111879-80-2'] |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Habanolide - Vigon](https://www.vigon.com/product/habanolide/) | trade/common name in title: 'habanolide' |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Page 1 ( 7 )](https://shop.perfumersapprentice.com/msds/6099.pdf) | trade/common name in text: 'habanolide'; CAS match ['111879-80-2'] |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [THE JOHN D. WALSH CO., INC.](https://www.johndwalsh.com/wp-content/uploads/2016/09/HABANOLIDE-SDS.pdf) | trade/common name in title: 'habanolide'; CAS match ['111879-80-2'] |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [Habanolide Subst (Fir)](https://www.hekserij.nl/wp-content/uploads/2024/10/SDS-23166-Habanolide-Subst-Fir-2024-03.pdf) — trade/common name in title: 'habanolide'; labelled CAS ['106-02-5'] not in master set ['111879-80-2']; name matches but CAS contradicts master -> CONFLICT revi…
- [SAFETY DATA SHEET](https://www.vigon.com/product/habanolide-substitute/?doc=MSDS%2F509446_vigon_sds_us_english.pdf&namee=HabanolideSubstituteSDS) — trade/common name in title: 'habanolide'; CAS match ['111879-80-2']; title describes a different product ('substitute'); title names another grade ('substitute…
- [Habanolide (Fir)](https://www.hekserij.nl/wp-content/uploads/2026/01/SDS-23238-Habanolide-Fir-2026-01.pdf) — trade/common name in title: 'habanolide'; labelled CAS ['34902-57-3'] not in master set ['111879-80-2']; name matches but CAS contradicts master -> CONFLICT re…
- [Product Specification](https://www.vigon.com/product/habanolide-substitute/?doc=PACKET%2F509446packet.pdf&namee=HabanolideSubstituteAllDocuments) — trade/common name in title: 'habanolide'; CAS match ['111879-80-2']; title describes a different product ('substitute'); title names another grade ('substitute…
- [PerfumersWorld](https://www.perfumersworld.com/ifra/MSDS/3XA09821.pdf) — trade/common name in text: 'habanolide'; name only in body text

**Confianza de identidad:** EXACT_NAME_MANUFACTURER (score 0.85)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 106-02-5 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| cas | 34902-57-3 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| vapour_pressure | 0.1 mm Hg 20 | 13.3322 Pa | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| vapour_pressure | 0.1 mm Hg 20 | 13.3322 Pa | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| logp | 5.29 | 5.29 log10 | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| logp | 5.45 | 5.45 log10 | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| logp | 5.29 | 5.29 log10 | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| logp | 5.45 | 5.45 log10 | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.johndwalsh.com |
| density | 0.96 | 0.96 g/cm3 (or SG, ~equal at 20-25 C) | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| density | 1.02 | 1.02 g/cm3 (or SG, ~equal at 20-25 C) | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.vigon.com |
| density | 963.55 kg/m³ Type: 'density' Temp.: 20,5 °C | 0.9635 g/cm3 | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| density | 0.961 – 0.971 | 0.966 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| density | 0.961-0.971 | 0.966 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| density | 0.96 | 0.96 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| density | 1.02 | 1.02 g/cm3 (or SG, ~equal at 20-25 C) | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.vigon.com |
| density | .969 mg /l Flash Point: >212F Part. Coeff (n-log Pow : 5.45(25C) |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.johndwalsh.com |
| flash_point | >100°C | 100.0 C | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| flash_point | >100 C | 100.0 C | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| flash_point | >200.0 F | 93.3 C | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| flash_point | >200.0 F | 93.3 C | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.vigon.com |
| flash_point | > 100 °C | 100.0 C | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| flash_point | >100 C | 100.0 C | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| flash_point | >200.0 F | 93.3 C | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| flash_point | 212°F (93°C) | 100.0 C | DISTRIBUTOR_SPEC | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| flash_point | > 93.5 °C | 93.5 C | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| flash_point | >93.5 C | 93.5 C | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| flash_point | >200 °F | 93.3 C | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.vigon.com |
| flash_point | >200 F | 93.3 C | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.vigon.com |
| flash_point | >200.0 F | 93.3 C | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.vigon.com |
| flash_point | >212 F | 100.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.johndwalsh.com |
| boiling_point | Greater than 100 C @ 25 mmHg | 100.0 C | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.perfumersworld.com |
| boiling_point | 100 C | 100.0 C | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.perfumersworld.com |
| boiling_point | 333 °C Atm. press.: 1013,3 hPa | 333.0 C | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| boiling_point | 333 C | 333.0 C | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| physical_state | Colorless to pale yellow Oily liquid |  | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.perfumersworld.com |
| physical_state | Liquid |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| solubility | Insoluble in water; soluble in alcohol. FLASH POINT (CC): Not determi… |  | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.perfumersworld.com |
| solubility | Materialnearlyinsolubleinwater. |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| solubility | Insoluble in water. |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| odour_description | Sweet and floral odour |  | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.perfumersworld.com |
| odour_description | Nodataavailable |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| product_code | 23238 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| h_statement | H317 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| h_statement | H411 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| h_statement | H400 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| h_statement | H410 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| h_statement | EUH208 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
| h_statement | H303 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| h_statement | H313 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| h_statement | H400 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| h_statement | H410 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| h_statement | H303 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| h_statement | H313 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| h_statement | H410 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| signal_word | Warning |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| signal_word | Warning |  | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.vigon.com |
| signal_word | Warning |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| signal_word | Warning |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| signal_word | Warning |  | DISTRIBUTOR_SDS | AMBIGUOUS | NEEDS_REVIEW | www.vigon.com |
| sds_product_name | Product form : Substance |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | www.hekserij.nl |
_… 32 claims más en data/staging.sqlite_

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** vapour_pressure=0.1 mm Hg 20 (DISTRIBUTOR_SDS, NEEDS_REVIEW); vapour_pressure=0.1 mm Hg 20 (RETAILER (SECONDARY CLAIM) SDS, VALID)
**SDS/CLP (por SDS, sin mezclar):** shop.perfumersapprentice.com: H303, H313, H400, H410, Warning · www.vigon.com: Warning

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] — valores: H303 [RETAILER]; H313 [RETAILER]; H400 [RETAILER]; H410 [RETAILER]; H303 [RETAILER]; H313 [RETAILER]; H410 [RETAILER]

**Cambios propuestos:** 7 (NEEDS_REVIEW: 7)

- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=vapor_pressure_supplier, value=13.3322, unit=Pa (converted from 0.1 mm hg (temperature not stated))
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=density_20C, value=0.96, unit=g/cm3 (or SG, ~equal at 20-25 C)
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=>93.3, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=100.0, unit=C
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H303, H313, H400, H410
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H303, H313, H410
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://studio.dsm-firmenich.com/product/habanolider-pe-947303): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Resolver conflicto en `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only]
- 5 documento(s) de identidad ambigua esperan revisión humana.

---

## S-0372 — FLORHYDRAL TOCO (ELINCS)

*Grupo piloto:* GIV_DSMF_SYM · *Qué prueba:* official manufacturer HTML (Givaudan structured page), CAS conflict in secondary sources
*Estado final:* **NEEDS_REVIEW** — 4 conflicts; 16 changes need review
*Master antes:* tier `B_EXACT_CHEMICAL_GRADE_UNCONFIRMED`, CAS `125109-85-5`, readiness 74 (READY_WITH_CAVEATS)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 81 (READY_WITH_CAVEATS); si se aprueban también los NEEDS_REVIEW → 81 (READY_WITH_CAVEATS)

**Queries realizadas**

- `claude_websearch` · Florhydral Givaudan → 10 resultados
- `claude_websearch` · Florhydral CAS 125109-85-5 → 10 resultados
- `claude_websearch` · Florhydral safety data sheet → 10 resultados
- `claude_websearch` · Florhydral use level → 9 resultados
- `claude_websearch` · Florhydral Givaudan pdf → 10 resultados
- `claude_websearch` · Florhydral odor vapor pressure → 9 resultados
- `claude_websearch` · Florhydral Vigon → 10 resultados
- `claude_websearch` · Florhydral TOCO → 10 resultados
- `pubchem_api` · cas:125109-85-5 → 0 resultados

**Fuentes encontradas:** 43 URLs distintas; 18 seleccionadas para descarga (FETCHED: 14, ENV_UNREACHABLE: 1, ROBOTS_DISALLOWED: 1, MANUAL_RETRIEVAL_REQUIRED: 2); 13 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://pellwall.com/products/florhydral — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: HTTPSConnectionPool(host='pell…)
- https://www.sciencedirect.com/science/article/abs/pii/S0957416602002021 — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.ulprospector.com/en/la/Food/Detail/33549/994497/Florhydral — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.ulprospector.com/en/la/PersonalCare/Detail/31182/994497/Florhydral — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| EXACT_GRADE | OFFICIAL_MANUFACTURER | UNKNOWN_LICENSE | [Florhydral™ / Givaudan](https://www.givaudan.com/fragrance-beauty/fragrance-ingredients-business/fragrance-molecules/florhydraltm) | trade/common name in title: 'florhydral'; CAS match ['125109-85-5']; official manufacturer domain (Givaudan); expected manufacturer 'Givaudan' mentioned |
| EXACT_NAME_MANUFACTURER | OFFICIAL_MANUFACTURER | UNKNOWN_LICENSE | [Demo Formulas](https://www.givaudan.com/files/1472023_formula.pdf) | trade/common name in text: 'florhydral'; official manufacturer domain (Givaudan); formula document -> formula pipeline (no material claims) |
| EXACT_NAME_MANUFACTURER | OFFICIAL_MANUFACTURER | UNKNOWN_LICENSE | [Demo Formulas](https://www.givaudan.com/files/1461553_formula.pdf) | trade/common name in text: 'florhydral'; official manufacturer domain (Givaudan); formula document -> formula pipeline (no material claims) |
| EXACT_NAME_MANUFACTURER | OFFICIAL_MANUFACTURER | UNKNOWN_LICENSE | [Print Page / Givaudan](https://www.givaudan.com/print/1314306) | trade/common name in text: 'florhydral'; CAS match ['125109-85-5']; official manufacturer domain (Givaudan); expected manufacturer 'Givaudan' mentioned |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Page 1 ( 7 )](https://shop.perfumersapprentice.com/msds/6085.pdf) | trade/common name in text: 'florhydral'; CAS match ['125109-85-5']; expected manufacturer 'Givaudan' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Perfumers Apprentice - Florhydral® (Givaudan) **](https://shop.perfumersapprentice.com/p-6085-florhydral-givaudan.aspx) | trade/common name in title: 'florhydral'; CAS match ['125109-85-5']; expected manufacturer 'Givaudan' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Floral Butanal / Florhydral® (67583-77-1) - Synthetic Ingre…](https://www.scentspiracy.com/fragrance-ingredients/p/floral-butanal) | trade/common name in title: 'florhydral'; CAS match ['125109-85-5']; expected manufacturer 'Givaudan' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Florhydral - BC Fragrance](https://shop.bcfragrance.com/product/florhydral-for-pre-order/) | trade/common name in title: 'florhydral'; CAS match ['125109-85-5']; expected manufacturer 'Givaudan' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Florhydral – Fraterworks](https://fraterworks.com/products/florhydral) | trade/common name in title: 'florhydral'; CAS match ['125109-85-5']; expected manufacturer 'Givaudan' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Florhydral from Givaudan-Aromatic Chemicals – Bulkaroma](https://bulkaroma.com/products/florhydral-givaudan) | trade/common name in title: 'florhydral'; CAS match ['125109-85-5']; expected manufacturer 'Givaudan' mentioned; manufacturer stated by a third party |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Product Specification](https://www.vigon.com/product/florhydral/?doc=PACKET%2F501126packet.pdf&namee=FlorhydralAllDocuments) | trade/common name in title: 'florhydral'; CAS match ['125109-85-5'] |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Florhydral - Vigon](https://www.vigon.com/product/florhydral/) | trade/common name in title: 'florhydral' |
| LIKELY_MATCH | IDENTITY_DB | PRODUCTION_SAFE_WITH_ATTRIBUTION | [Florhydral / C13H18O / CID 86209 - PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/Florhydral) | trade/common name in title: 'florhydral' |

**Confianza de identidad:** EXACT_GRADE (score 0.95)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 125109-85-5 |  | MANUFACTURER | EXACT_GRADE | VALID | www.givaudan.com |
| cas | 125109-85-5 |  | MANUFACTURER | EXACT_NAME_MANUFACTURER | VALID | www.givaudan.com |
| cas | 125109-85-5 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| cas | 125109-85-5 |  | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| use_level | 0.2% - 2% | 0.2–2.0 % | MANUFACTURER | EXACT_GRADE | VALID_DISPUTED | www.givaudan.com |
| use_level | 0.2-2% | 0.2–2.0 % | MANUFACTURER | EXACT_GRADE | VALID_DISPUTED | www.givaudan.com |
| use_level | 0.2% - 2% | 0.2–2.0 % | MANUFACTURER | EXACT_NAME_MANUFACTURER | VALID_DISPUTED | www.givaudan.com |
| use_level | 0.2-2% | 0.2–2.0 % | MANUFACTURER | EXACT_NAME_MANUFACTURER | VALID_DISPUTED | www.givaudan.com |
| use_level | 5-7% | 5.0–7.0 % | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | CONFLICT | www.scentspiracy.com |
| vapour_pressure | 0.0200 hPa | 2.0 Pa | MANUFACTURER | EXACT_GRADE | VALID_DISPUTED | www.givaudan.com |
| vapour_pressure | 0.0200 hPa | 2.0 Pa | MANUFACTURER | EXACT_NAME_MANUFACTURER | VALID_DISPUTED | www.givaudan.com |
| vapour_pressure | 0.0065 hPa (68 °F/ 20 °C, OECD 104) | 0.65 Pa | DISTRIBUTOR_SDS | LIKELY_MATCH | CONFLICT | www.vigon.com |
| vapour_pressure | 0.0065 hPa | 0.65 Pa | DISTRIBUTOR_SDS | LIKELY_MATCH | CONFLICT | www.vigon.com |
| vapour_pressure | 110 kPa 50 | 110000.0 Pa | DISTRIBUTOR_SDS | LIKELY_MATCH | REJECTED | www.vigon.com |
| vapour_pressure | 0.0200 hPa (0.65 Pa at 20°C) | 2.0 Pa | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | CONFLICT | www.scentspiracy.com |
| vapour_pressure | 0.0200 hPa | 2.0 Pa | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | CONFLICT | www.scentspiracy.com |
| vapour_pressure | 0.02 hPa | 2.0 Pa | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | CONFLICT | www.scentspiracy.com |
| logp | 3,8 | 3.8 log10 | MANUFACTURER | EXACT_GRADE | VALID_DISPUTED | www.givaudan.com |
| logp | 3,8 | 3.8 log10 | MANUFACTURER | EXACT_NAME_MANUFACTURER | VALID_DISPUTED | www.givaudan.com |
| logp | 3.1 | 3.1 log10 | DISTRIBUTOR_SDS | LIKELY_MATCH | CONFLICT | www.vigon.com |
| logp | 3.8 | 3.8 log10 | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | CONFLICT | www.scentspiracy.com |
| tenacity | 1 week | 168.0 hours | MANUFACTURER | EXACT_GRADE | VALID | www.givaudan.com |
| tenacity | 1 week | 168.0 hours | MANUFACTURER | EXACT_NAME_MANUFACTURER | VALID | www.givaudan.com |
| tenacity | 1 week | 168.0 hours | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | shop.bcfragrance.com |
| tenacity | Lasts > 144 hours on a smelling strip. | 144.0 hours | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| substantivity_application | 5/5 stars | 5.0 stars (0-5, manufacturer scale) | MANUFACTURER | EXACT_GRADE | VALID | www.givaudan.com |
| substantivity_application | ★★★★★ |  | MANUFACTURER | EXACT_GRADE | VALID | www.givaudan.com |
| substantivity_application | 5/5 stars | 5.0 stars (0-5, manufacturer scale) | MANUFACTURER | EXACT_NAME_MANUFACTURER | VALID | www.givaudan.com |
| substantivity_application | ★★★★★ |  | MANUFACTURER | EXACT_NAME_MANUFACTURER | VALID | www.givaudan.com |
| density | 950.28 kg/m³ (68 °F/ 20 °C) | 0.9503 g/cm3 | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| density | 0.935–0.954 g/cm³ at 25°C | 0.9445 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | www.scentspiracy.com |
| density | 0.935-0.954 | 0.9445 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | www.scentspiracy.com |
| refractive_index | 1.504–1.508 (n²⁰D) | 1.506 nD | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | www.scentspiracy.com |
| refractive_index | 1.504-1.508 | 1.506 nD | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | www.scentspiracy.com |
| flash_point | 154 °F / 67.8 °C | 67.8 C | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | CONFLICT | shop.perfumersapprentice.com |
| flash_point | 154 F | 67.8 C | RETAILER (SECONDARY CLAIM) SDS | EXACT_NAME_MANUFACTURER | CONFLICT | shop.perfumersapprentice.com |
| flash_point | 154 °F | 67.8 C | DISTRIBUTOR_SDS | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| flash_point | 154 °F (68 °C, Pensky-Martens closed cup) | 67.8 C | DISTRIBUTOR_SDS | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| flash_point | 154 F | 67.8 C | DISTRIBUTOR_SDS | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| flash_point | 154°F (68°C) | 67.8 C | DISTRIBUTOR_SPEC | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| flash_point | 103.6°C (68°C) | 103.6 C | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | CONFLICT | www.scentspiracy.com |
| flash_point | 103.6 C | 103.6 C | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | CONFLICT | www.scentspiracy.com |
| boiling_point | 257 | 257.0 C | MANUFACTURER | EXACT_GRADE | VALID | www.givaudan.com |
| boiling_point | 257 | 257.0 C | MANUFACTURER | EXACT_NAME_MANUFACTURER | VALID | www.givaudan.com |
| boiling_point | 257 °C (495 °F, 1013 hPa) | 257.0 C | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| boiling_point | 257 C | 257.0 C | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| boiling_point | 257°C | 257.0 C | DISTRIBUTOR_SPEC | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| boiling_point | 251.3°C at 760 mmHg (257°C) | 251.3 C | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | www.scentspiracy.com |
| boiling_point | 251.3 C | 251.3 C | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | www.scentspiracy.com |
| boiling_point | 257ºC | 257.0 C | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | shop.bcfragrance.com |
| physical_state | Colourless Liquid |  | MANUFACTURER | EXACT_GRADE | VALID | www.givaudan.com |
| physical_state | Colourless Liquid |  | MANUFACTURER | EXACT_NAME_MANUFACTURER | VALID | www.givaudan.com |
| physical_state | Liquid |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| physical_state | As per product specification. |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| physical_state | Colourless liquid |  | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | shop.bcfragrance.com |
| physical_state | Clear Liquid |  | RETAILER (SECONDARY CLAIM) | EXACT_NAME_MANUFACTURER | VALID | fraterworks.com |
| solubility | Water: 40 mg/l (68 °F/ 20 °C) |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| odour_description | Florhydral™ has a very floral, fresh, natural odour (such as lily of … |  | MANUFACTURER | EXACT_GRADE | VALID | www.givaudan.com |
| odour_description | Florhydral™ has a very floral, fresh, natural odour (such as lily of … |  | MANUFACTURER | EXACT_NAME_MANUFACTURER | VALID | www.givaudan.com |
| odour_description | Floral Green Fresh Marine |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
_… 27 claims más en data/staging.sqlite_

**Evidencia de dosis:** 0.2% - 2% (MANUFACTURER, www.givaudan.com, VALID_DISPUTED); 0.2-2% (MANUFACTURER, www.givaudan.com, VALID_DISPUTED); 0.2% - 2% (MANUFACTURER, www.givaudan.com, VALID_DISPUTED); 0.2-2% (MANUFACTURER, www.givaudan.com, VALID_DISPUTED); 5-7% (RETAILER (SECONDARY CLAIM), www.scentspiracy.com, CONFLICT)
**Evidencia de performance:** vapour_pressure=0.0200 hPa (MANUFACTURER, VALID_DISPUTED); tenacity=1 week (MANUFACTURER, VALID); substantivity_application=5/5 stars (MANUFACTURER, VALID); substantivity_application=★★★★★ (MANUFACTURER, VALID); vapour_pressure=0.0200 hPa (MANUFACTURER, VALID_DISPUTED); tenacity=1 week (MANUFACTURER, VALID); substantivity_application=5/5 stars (MANUFACTURER, VALID); substantivity_application=★★★★★ (MANUFACTURER, VALID); vapour_pressure=0.0065 hPa (68 °F/ 20 °C, OEC… (DISTRIBUTOR_SDS, CONFLICT); vapour_pressure=0.0065 hPa (DISTRIBUTOR_SDS, CONFLICT); vapour_pressure=110 kPa 50 (DISTRIBUTOR_SDS, REJECTED); vapour_pressure=0.0200 hPa (0.65 Pa at 20°C) (RETAILER (SECONDARY CLAIM), CONFLICT); vapour_pressure=0.0200 hPa (RETAILER (SECONDARY CLAIM), CONFLICT); vapour_pressure=0.02 hPa (RETAILER (SECONDARY CLAIM), CONFLICT); tenacity=1 week (RETAILER (SECONDARY CLAIM), VALID); tenacity=Lasts > 144 hours on a smelli… (RETAILER (SECONDARY CLAIM), VALID)
**SDS/CLP (por SDS, sin mezclar):** shop.perfumersapprentice.com: Warning · www.vigon.com: Aquatic Acute 2, Aquatic Chronic 2, Flam. Liq. 4, H227, H401, H411

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `vapour_pressure`: vapour_pressure: independent sources disagree beyond tolerance ('rel', 0.3) [lower-tier dissent only] — valores: 0.0200 hPa [OFFICIAL_MANUFACTURER]; 0.0200 hPa [OFFICIAL_MANUFACTURER]; 0.0065 hPa (68 °F/ 20 °C, OECD 104) [DISTRIBUTOR]; 0.0065 hPa [DISTRIBUTOR]; 0.0200 hPa (0.65 Pa at 20°C) [RETAILER]; 0.0200 hPa [RETAILER]; 0.02 hPa [RETAILER]
- `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only] — valores: 154 °F / 67.8 °C [RETAILER]; 154 F [RETAILER]; 154 °F [DISTRIBUTOR]; 154 °F (68 °C, Pensky-Martens closed cu… [DISTRIBUTOR]; 154 F [DISTRIBUTOR]; 154°F (68°C) [DISTRIBUTOR]; 103.6°C (68°C) [RETAILER]; 103.6 C [RETAILER]
- `logp`: logp: independent sources disagree beyond tolerance ('abs', 0.6) [lower-tier dissent only] — valores: 3,8 [OFFICIAL_MANUFACTURER]; 3,8 [OFFICIAL_MANUFACTURER]; 3.1 [DISTRIBUTOR]; 3.8 [RETAILER]
- `use_level`: recommended use levels from independent sources do not agree [lower-tier dissent only] — valores: 0.2% - 2% [OFFICIAL_MANUFACTURER]; 0.2-2% [OFFICIAL_MANUFACTURER]; 0.2% - 2% [OFFICIAL_MANUFACTURER]; 0.2-2% [OFFICIAL_MANUFACTURER]; 5-7% [RETAILER]

**Cambios propuestos:** 23 (NEEDS_REVIEW: 15, BLOCKED_CONFLICT: 3, AUTO_ELIGIBLE: 5)

- `NEEDS_REVIEW` · DOSE EVIDENCE STRUCTURED · APPEND_ROW · dose_type=SUPPLIER_RECOMMENDATION, value_text=0.2% - 2%, unit=%
- `BLOCKED_CONFLICT` · DOSE EVIDENCE STRUCTURED · APPEND_ROW · dose_type=SECONDARY_REFERENCE_MAX_USE, value_text=5-7%, unit=%
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=vapor_pressure_supplier, value=2.0, unit=Pa (converted from 0.0200 hpa (temperature not stated))
- `BLOCKED_CONFLICT` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=vapor_pressure_supplier, value=0.65, unit=Pa (converted from 0.0065 hpa at 20 C)
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=logP_supplier, value=3.8, unit=log10
- `BLOCKED_CONFLICT` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=logP_supplier, value=3.1, unit=log10
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=density_20C, value=0.9503, unit=g/cm3
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=67.8, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=67.8, unit=C
- `AUTO_ELIGIBLE` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=boiling_point_normal, value=257.0, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=boiling_point_normal, value=257.0, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=boiling_point_normal, value=257.0, unit=C
- `AUTO_ELIGIBLE` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=physical_state, value=Colourless Liquid
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=physical_state, value=Liquid
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=solubility, value=Water: 40 mg/l (68 °F/ 20 °C)
- `AUTO_ELIGIBLE` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=168.0, unit=hours
- `NEEDS_REVIEW` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=168.0, unit=hours
- `NEEDS_REVIEW` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=>144.0, unit=hours
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · NOTE_ONLY · odour_description_manufacturer=Florhydral™ has a very floral, fresh, natural odour (such as lily of the valley, hyacinth...). Its great int…
- `AUTO_ELIGIBLE` · MATERIAL IDENTITY · UPDATE_CELL · identity_tier: B_EXACT_CHEMICAL_GRADE_UNCONFIRMED → A_EXACT_COMMERCIAL_GRADE
- `AUTO_ELIGIBLE` · MATERIAL IDENTITY · UPDATE_CELL · supplier_grade_url: None → https://www.givaudan.com/fragrance-beauty/fragrance-ingredients-business/fragrance-molecules/florhydraltm
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes=Aquatic Acute 2; Aquatic Chronic 2; Flam. Liq. 4 | H: H227, H401, H411
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=FOUND

**Preguntas abiertas**

- Resolver conflicto en `vapour_pressure`: vapour_pressure: independent sources disagree beyond tolerance ('rel', 0.3) [lower-tier dissent only]
- Resolver conflicto en `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only]
- Resolver conflicto en `logp`: logp: independent sources disagree beyond tolerance ('abs', 0.6) [lower-tier dissent only]
- Resolver conflicto en `use_level`: recommended use levels from independent sources do not agree [lower-tier dissent only]

---

## S-0502 — TIMBEROL

*Grupo piloto:* GIV_DSMF_SYM · *Qué prueba:* Symrise, NOT_READY, downgraded Tier A->B in audit
*Estado final:* **NEEDS_REVIEW** — 0 conflicts; 2 changes need review
*Master antes:* tier `B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK`, CAS `70788-30-6`, readiness 41 (NOT_READY)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 61 (PARTIAL); si se aprueban también los NEEDS_REVIEW → 61 (PARTIAL)

**Queries realizadas**

- `claude_websearch` · Timberol Symrise → 9 resultados
- `claude_websearch` · Timberol CAS 70788-30-6 → 10 resultados
- `claude_websearch` · Timberol safety data sheet → 10 resultados
- `claude_websearch` · Timberol use level → 10 resultados
- `claude_websearch` · Timberol Symrise pdf → 9 resultados
- `claude_websearch` · Timberol odor vapor pressure → 9 resultados
- `claude_websearch` · Timberol Norlimbanol difference → 9 resultados
- `claude_websearch` · Timberol Ventos → 9 resultados
- `pubchem_api` · cas:70788-30-6 → 0 resultados

**Fuentes encontradas:** 54 URLs distintas; 24 seleccionadas para descarga (FETCHED: 14, ROBOTS_DISALLOWED: 8, ENV_UNREACHABLE: 1, MANUAL_RETRIEVAL_REQUIRED: 1); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://cosmetics.specialchem.com/product/i-symrise-timberol — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.scentree.co/en/Timberol%C2%AE.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /en/Timberol%C2%AE.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://www.thegoodscentscompany.com/data/rw1020712.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/rw1020712.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://labelsds.com/images/user_uploads/Tim-bor%20Label%204-1-20.pdf — ROBOTS_DISALLOWED (robots.txt disallows PerrocoLabResearchBot for /images/user_uploads/Tim-bor%20Label%204-1…)
- http://olaughlinco.com/uploads/202411/11/SDS_TIMBEROL%20V1.pdf — ENV_UNREACHABLE (domain unreachable earlier in run: ConnectionError: HTTPConnectionPool(host='olaughlinco.…)
- https://sds.rentokil-initial.com/sds/files/US-Pest-Timbor_(EPA_64405_8)_SDS-EN.pdf — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://basenotes.com/threads/woods-norlimbanol-timberol.295280/ — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.researchgate.net/publication/287482401_TimberolR_Inhibits_TAAR5-Mediated_Responses_to_Trimethylamine_and_Influences_the_Olfactory_Threshold_in_Humans — MANUAL_RETRIEVAL_REQUIRED (HTTP 403 (site refuses automated access; not bypassed))
- https://www.specialchem.com/cosmetics/product/symrise-timberol — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://basenotes.com/community/threads/woods-norlimbanol-timberol.295280/ — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| EXACT_GRADE | OFFICIAL_MANUFACTURER | UNKNOWN_LICENSE | [stneidergnI](https://www.symrise.com/fileadmin/symrise/Marketing/Scent_and_care/Aroma_molecules/Ingredient_finder/SYM_PC_Datenblaetter/SYM_PC-Timberol.pdf) | trade/common name in title: 'timberol'; CAS match ['70788-30-6']; official manufacturer domain (Symrise); expected manufacturer 'Symrise' mentioned |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Timberol (CAS 57641-67-3) – Dry Amber-Woody Fixative Synthe…](https://www.scentspiracy.com/fragrance-ingredients/p/timberol) | trade/common name in title: 'timberol'; expected manufacturer 'Symrise' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Timberol - SYMRISE – Bulkaroma](https://bulkaroma.com/products/timberol-symrise) | trade/common name in title: 'timberol'; CAS match ['70788-30-6']; expected manufacturer 'Symrise' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Woodamber from Indian Manufacturer-Aromatic Chemicals – Bul…](https://bulkaroma.com/products/woodamber-timberol-equivalent-padmini) | trade/common name in title: 'timberol'; CAS match ['70788-30-6']; expected manufacturer 'Symrise' mentioned; manufacturer stated by a third party |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://www.vigon.com/product/tabanon/?doc=MSDS/502539_vigon_sds_us_english.pdf&namee=TabanonSDS) | trade/common name in text: 'timberol'; CAS match ['70788-30-6'] |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [WOODAMBER / TIMBEROL](https://www.ventos.com/index.php/en/producto/5327/WOODAMBER+-+TIMBEROL/223) | trade/common name in title: 'timberol'; CAS match ['70788-30-6'] |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [WOODAMBER / TIMBEROL / Noves fitxes EN](https://www.ventos.com/en/producto/5327/essential) | trade/common name in title: 'timberol'; CAS match ['70788-30-6'] |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Timberol /](https://www.perfumersworld.com/view.php?pro_id=3WW07134) | trade/common name in title: 'timberol'; CAS match ['70788-30-6'] |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Norlimbanol Dextro /](https://www.perfumersworld.com/view.php?pro_id=4WU22432) | trade/common name in text: 'timberol'; CAS match ['70788-30-6'] |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [Norlimbanol® – Fraterworks](https://fraterworks.com/products/norlimbanol) — trade/common name in text: 'timberol'; CAS match ['70788-30-6']; page is about another trade product ('Norlimbanol'); same CAS/name mention but a different com…
- [Norlimbanol® Dextro – Fraterworks](https://fraterworks.com/products/norlimbanol-dextro) — trade/common name in text: 'timberol'; CAS match ['70788-30-6']; page is about another trade product ('Norlimbanol'); same CAS/name mention but a different com…
- [Perfumers Apprentice - Norlimbanol® (Firmenich) **](https://shop.perfumersapprentice.com/p-7397-norlimbanol-firmenich.aspx) — trade/common name in text: 'timberol'; CAS match ['70788-30-6']; expected manufacturer 'Symrise' mentioned; page is about another trade product ('fumers Appren…

**Fuentes rechazadas:** 2

- Preparation of Treatment Solutions — neither trade name nor CAS found
- MATERIAL SAFETY DATA SHEET — neither trade name nor CAS found

**Confianza de identidad:** EXACT_GRADE (score 0.95)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 70788-30-6 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| cas | 70788-30-6 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| use_level | 0.1-3% | 0.1–3.0 % | MANUFACTURER | EXACT_GRADE | VALID | www.symrise.com |
| vapour_pressure | 0.0005 mm Hg 25 | 0.066661 Pa | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| logp | 5.80 | 5.8 log10 | MANUFACTURER | EXACT_GRADE | VALID | www.symrise.com |
| tenacity | Lasts > 2 weeks on a smelling strip. | 336.0 hours | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| tenacity | Lasts > 2 weeks on a smelling strip. | 336.0 hours | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| flash_point | >100 C | 100.0 C | MANUFACTURER | EXACT_GRADE | VALID | www.symrise.com |
| flash_point | >200.0 F | 93.3 C | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| physical_state | Colourless viscous liquid |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| physical_state | Colourless viscous liquid |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| signal_word | Warning |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| sds_component_cas | 70788-30-6 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| storage | store near an open flame, heat or other sources of ignition. |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| stability_text | stable and non-reactive under normal conditions of use, storage and t… |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |

**Evidencia de dosis:** 0.1-3% (MANUFACTURER, www.symrise.com, VALID)
**Evidencia de performance:** vapour_pressure=0.0005 mm Hg 25 (DISTRIBUTOR_SDS, NEEDS_REVIEW); tenacity=Lasts > 2 weeks on a smelling… (RETAILER (SECONDARY CLAIM), NEEDS_REVIEW); tenacity=Lasts > 2 weeks on a smelling… (RETAILER (SECONDARY CLAIM), NEEDS_REVIEW)
**SDS/CLP (por SDS, sin mezclar):** www.vigon.com: Warning

**Cambios propuestos:** 8 (AUTO_ELIGIBLE: 5, NEEDS_REVIEW: 3)

- `AUTO_ELIGIBLE` · DOSE EVIDENCE STRUCTURED · APPEND_ROW · dose_type=SUPPLIER_RECOMMENDATION, value_text=0.1-3%, unit=%
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=vapor_pressure_supplier, value=0.066661, unit=Pa (converted from 0.0005 mm hg (temperature not stated))
- `AUTO_ELIGIBLE` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=logP_supplier, value=5.8, unit=log10
- `AUTO_ELIGIBLE` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=>100.0, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=>93.3, unit=C
- `AUTO_ELIGIBLE` · MATERIAL IDENTITY · UPDATE_CELL · identity_tier: B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK → A_EXACT_COMMERCIAL_GRADE
- `AUTO_ELIGIBLE` · MATERIAL IDENTITY · UPDATE_CELL · supplier_grade_url: None → https://www.symrise.com/fileadmin/symrise/Marketing/Scent_and_care/Aroma_molecules/Ingredient_finder/SYM_PC_Date…
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=FOUND

**Preguntas abiertas**

- Sin SDS del producto analizable: pedir SDS al proveedor/escuela.
- 3 documento(s) de identidad ambigua esperan revisión humana.

---

## S-0366 — CALONE

*Grupo piloto:* GIV_DSMF_SYM · *Qué prueba:* Calone 1951 vs generic molecule, IFRA 52 pending
*Estado final:* **NEEDS_REVIEW** — 3 conflicts; 13 changes need review
*Master antes:* tier `B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK`, CAS `28940-11-6`, readiness 48 (PARTIAL)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 48 (PARTIAL); si se aprueban también los NEEDS_REVIEW → 48 (PARTIAL)

**Queries realizadas**

- `claude_websearch` · Calone 1951 Firmenich → 10 resultados
- `claude_websearch` · Calone CAS 28940-11-6 → 10 resultados
- `claude_websearch` · Calone 1951 safety data sheet → 9 resultados
- `claude_websearch` · Calone use level → 9 resultados
- `claude_websearch` · Calone dsm-firmenich → 9 resultados
- `claude_websearch` · Calone Firmenich pdf → 10 resultados
- `claude_websearch` · Calone odor vapor pressure → 10 resultados
- `claude_websearch` · Calone 1951 Vigon → 9 resultados
- `pubchem_api` · cas:28940-11-6 → 0 resultados

**Fuentes encontradas:** 53 URLs distintas; 21 seleccionadas para descarga (FETCHED: 14, MANUAL_RETRIEVAL_REQUIRED: 1, ROBOTS_DISALLOWED: 6); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://www.ulprospector.com/en/na/PersonalCare/Detail/31183/994880/Calone-1951 — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.specialchem.com/cosmetics/product/dsm-firmenich-calone — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.specialchem.com/cosmetics/product/dsm-firmenich-cascalone — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://studio.dsm-firmenich.com/product/cascaloner-pe-920000 — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://cosmetics.specialchem.com/product/i-firmenich-calone — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.firmenich.com/sites/default/files/uploads/files/ingredients/marketing-sheet/perfumery/CALONE_918970.pdf — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.firmenich.com/sites/default/files/uploads/files/ingredients/sharing_innovation/CASCALONE.pdf — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Perfumers Apprentice - Calone 1951® (Firmenich) **](https://shop.perfumersapprentice.com/p-6021-calone-1951-firmenich.aspx) | trade/common name in title: 'calone 1951'; CAS match ['28940-11-6']; expected manufacturer 'dsm-firmenich' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Calone (28940-11-6) — Premium Marine Synthetic Ingredient f…](https://www.scentspiracy.com/fragrance-ingredients/p/calone) | trade/common name in title: 'calone'; CAS match ['28940-11-6']; expected manufacturer 'dsm-firmenich' mentioned; manufacturer stated by a third party |
| EXACT_NAME_MANUFACTURER | RETAILER | RESEARCH_ONLY | [Perfumers Apprentice - Calone® 10% (Firmenich) (DPG)](https://shop.perfumersapprentice.com/p-8228-calone-10-firmenich-dpg.aspx) | trade/common name in title: 'calone'; CAS match ['28940-11-6']; expected manufacturer 'dsm-firmenich' mentioned; manufacturer stated by a third party |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://www.vigon.com/product/calone-1951/?doc=MSDS%2F503181_vigon_sds_us_english.pdf&namee=Calone1951SDS) | trade/common name in title: 'calone'; CAS match ['28940-11-6'] |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Calone 1951 - Vigon](https://www.vigon.com/product/calone-1951/) | trade/common name in title: 'calone 1951' |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Product Specification](https://www.vigon.com/product/calone-1951/?doc=PACKET/503181packet.pdf&namee=Calone1951AllDocuments) | trade/common name in title: 'calone'; CAS match ['28940-11-6'] |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Heavy Metals and Pesticide Statement](https://www.vigon.com/product/calone-1951/?doc=HEAMET%2F503181heamet.pdf&namee=Calone1951PesticidesMetals) | trade/common name in title: 'calone' |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [The John D. Walsh Company, Inc.](https://perfumersupplyhouse.com/wp-content/uploads/2014/04/CALONE-1951-MSDS.pdf) | trade/common name in title: 'calone'; CAS match ['28940-11-6'] |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [MATERIAL SAFETY DATA SHEET](http://www.mu-intel.com/upload/msds/20140101034908.pdf) | trade/common name in text: 'calone 1951'; CAS match ['28940-11-6'] |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Calone](https://www.chemtexusa.com/wp-content/uploads/2021/03/C0150_Calone.pdf) | trade/common name in title: 'calone'; CAS match ['28940-11-6'] |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Material Safety Data Sheet (MSDS)](https://www.chemicalbull.com/images/product/MSDS-1759302468.pdf) | trade/common name in text: 'watermelon ketone'; CAS match ['28940-11-6'] |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [Calone 1951 (Fir) *ADR* Online Kopen bij Hekserij](https://eng.hekserij.nl/shop/fragrance-raw-material/search-by-type/aroma-chemicals/calone-1951-fir/) — trade/common name in title: 'calone 1951'; CAS match ['28940-11-6']; expected manufacturer 'dsm-firmenich' mentioned; title describes a different product ('typ…

**Fuentes rechazadas:** 2

- Noves fitxes EN — neither trade name nor CAS found; NO_CONTENT: only site template after removing 371 shared lines (page likely…
- Noves fitxes EN — neither trade name nor CAS found; NO_CONTENT: only site template after removing 371 shared lines (page likely…

**Confianza de identidad:** EXACT_NAME_MANUFACTURER (score 0.80)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 28940-11-6 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| cas | 28940-11-6 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| cas | 28940-11-6 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| use_level | 0,1-2% | 0.1–2.0 % | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| vapour_pressure | 1 mm Hg 20 | 133.322 Pa | DISTRIBUTOR_SDS | LIKELY_MATCH | CONFLICT | www.vigon.com |
| vapour_pressure | 0.87 Pa (25°C, OECD 104) | 0.87 Pa | DISTRIBUTOR_SDS | LIKELY_MATCH | CONFLICT | www.vigon.com |
| vapour_pressure | 0.87 Pa 25 | 0.87 Pa | DISTRIBUTOR_SDS | LIKELY_MATCH | CONFLICT | www.vigon.com |
| vapour_pressure | 1.0 mmHg @ 20 °C | 133.322 Pa | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | perfumersupplyhouse.com |
| vapour_pressure | 1.0 mmHg 20 | 133.322 Pa | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | perfumersupplyhouse.com |
| vapour_pressure | 0,87 Pa | 0.87 Pa | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| logp | 1.95 | 1.95 log10 | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| logp | 1,95 | 1.95 log10 | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| density | 1.353 (21.6°C, OECD 109) | 1.353 g/cm3 (or SG, ~equal at 20-25 C) | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| density | 1.353 | 1.353 g/cm3 (or SG, ~equal at 20-25 C) | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| density | >1 @ 25 °C |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | perfumersupplyhouse.com |
| density | 1,35 | 1.35 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| flash_point | >200.0 F | 93.3 C | DISTRIBUTOR_SDS | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| flash_point | 212°F (100°C) | 100.0 C | DISTRIBUTOR_SPEC | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| flash_point | >200 °F | 93.3 C | DISTRIBUTOR_SDS | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| flash_point | > 212 °F (100°C, Closed cup) | 100.0 C | DISTRIBUTOR_SDS | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| flash_point | > 212 °F | 100.0 C | DISTRIBUTOR_SDS | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| flash_point | >200 F | 93.3 C | DISTRIBUTOR_SDS | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| flash_point | >212 F | 100.0 C | DISTRIBUTOR_SDS | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| flash_point | >93 C | 93.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | perfumersupplyhouse.com |
| flash_point | 167 Method Used: CC |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.mu-intel.com |
| flash_point | > 200 °C | 200.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | www.chemtexusa.com |
| flash_point | >200 C | 200.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | www.chemtexusa.com |
| flash_point | 118 C | 118.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | www.chemicalbull.com |
| boiling_point | 267°C | 267.0 C | DISTRIBUTOR_SPEC | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| boiling_point | 267 °C (OECD 103) | 267.0 C | DISTRIBUTOR_SDS | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| boiling_point | 267 C | 267.0 C | DISTRIBUTOR_SDS | LIKELY_MATCH | VALID_DISPUTED | www.vigon.com |
| boiling_point | 70 Specific Gravity @ 25C (H20=1.0): N/A | 70.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | REJECTED | www.mu-intel.com |
| boiling_point | 300 C | 300.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | www.chemicalbull.com |
| boiling_point | 267 °C | 267.0 C | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| boiling_point | 267 C | 267.0 C | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| physical_state | Solid |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| physical_state | Crystalline powder. |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| physical_state | White solid. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | perfumersupplyhouse.com |
| physical_state | SOLID Odor: FRESH,MARINE,GREEN,FRUITY |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.mu-intel.com |
| physical_state | Solid |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| solubility | Water: 13700 mg/l (20°C, OECD 105) |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| solubility | SLIGHT Melting Point (°C): 38 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.mu-intel.com |
| odour_description | Characteristic strong odour according to the commercial description o… |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| product_code | 503181 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| product_code | 503181 ID # : EXAMPLE Liters: 0.000 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| product_code | C0150 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemtexusa.com |
| product_code | 23070 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| ec_number | 249-320-4 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| origin | IRELAND |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| origin | Ireland |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| clp_class | Skin Corr. 1B |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| clp_class | Eye Dam. 1 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| clp_class | STOT SE 3 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| h_statement | H314 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| h_statement | H318 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| h_statement | H336 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| signal_word | None |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| signal_word | Warning |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemicalbull.com |
| sds_product_name | 503181 Calone 1951 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| sds_product_name | CALONE 1951 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | perfumersupplyhouse.com |
_… 17 claims más en data/staging.sqlite_

**Evidencia de dosis:** 0,1-2% (RETAILER (SECONDARY CLAIM), eng.hekserij.nl, NEEDS_REVIEW)
**Evidencia de performance:** vapour_pressure=1 mm Hg 20 (DISTRIBUTOR_SDS, CONFLICT); vapour_pressure=0.87 Pa (25°C, OECD 104) (DISTRIBUTOR_SDS, CONFLICT); vapour_pressure=0.87 Pa 25 (DISTRIBUTOR_SDS, CONFLICT); vapour_pressure=1.0 mmHg @ 20 °C (SECONDARY_REFERENCE SDS, CONFLICT); vapour_pressure=1.0 mmHg 20 (SECONDARY_REFERENCE SDS, CONFLICT); vapour_pressure=0,87 Pa (RETAILER (SECONDARY CLAIM), NEEDS_REVIEW)
**SDS/CLP (por SDS, sin mezclar):** www.chemicalbull.com: Warning · www.vigon.com: Eye Dam. 1, H314, H318, H336, None, STOT SE 3, Skin Corr. 1B

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `vapour_pressure`: vapour_pressure: independent sources disagree beyond tolerance ('rel', 0.3) — valores: 1 mm Hg 20 [DISTRIBUTOR]; 0.87 Pa (25°C, OECD 104) [DISTRIBUTOR]; 0.87 Pa 25 [DISTRIBUTOR]; 1.0 mmHg @ 20 °C [SECONDARY]; 1.0 mmHg 20 [SECONDARY]
- `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only] — valores: >200.0 F [DISTRIBUTOR]; 212°F (100°C) [DISTRIBUTOR]; >200 °F [DISTRIBUTOR]; > 212 °F (100°C, Closed cup) [DISTRIBUTOR]; > 212 °F [DISTRIBUTOR]; >200 F [DISTRIBUTOR]; >212 F [DISTRIBUTOR]; >93 C [SECONDARY]
- `boiling_point`: boiling_point: independent sources disagree beyond tolerance ('abs', 8) [lower-tier dissent only] — valores: 267°C [DISTRIBUTOR]; 267 °C (OECD 103) [DISTRIBUTOR]; 267 C [DISTRIBUTOR]; 300 C [SECONDARY]

**Cambios propuestos:** 14 (NEEDS_REVIEW: 12, BLOCKED_CONFLICT: 2)

- `NEEDS_REVIEW` · DOSE EVIDENCE STRUCTURED · APPEND_ROW · dose_type=SECONDARY_REFERENCE_MAX_USE, value_text=0,1-2%, unit=%
- `BLOCKED_CONFLICT` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=vapor_pressure_supplier, value=133.322, unit=Pa (converted from 1 mm hg (temperature not stated))
- `BLOCKED_CONFLICT` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=vapor_pressure_supplier, value=0.87, unit=Pa (converted from 0.87 pa at 25 C)
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=logP_supplier, value=1.95, unit=log10
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=density_20C, value=1.353, unit=g/cm3 (or SG, ~equal at 20-25 C)
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=>93.3, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=100.0, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=>93.3, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=boiling_point_normal, value=267.0, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=boiling_point_normal, value=267.0, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=physical_state, value=Solid
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=solubility, value=Water: 13700 mg/l (20°C, OECD 105)
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes=Eye Dam. 1; STOT SE 3; Skin Corr. 1B | H: H314, H318, H336
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://studio.dsm-firmenich.com/product/cascaloner-pe-920000): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Resolver conflicto en `vapour_pressure`: vapour_pressure: independent sources disagree beyond tolerance ('rel', 0.3)
- Resolver conflicto en `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only]
- Resolver conflicto en `boiling_point`: boiling_point: independent sources disagree beyond tolerance ('abs', 8) [lower-tier dissent only]
- 1 documento(s) de identidad ambigua esperan revisión humana.

---

## N-0775 — VETIVER OIL LMR

*Grupo piloto:* NATURAL · *Qué prueba:* natural GC-MS, ISO 4716, REFERENCE_COMPOSITION
*Estado final:* **NEEDS_REVIEW** — 2 conflicts; 4 changes need review
*Master antes:* tier `C_GENERIC_NATURAL_REFERENCE`, CAS `8016-96-4`, readiness 48 (PARTIAL)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 48 (PARTIAL); si se aprueban también los NEEDS_REVIEW → 48 (PARTIAL)

**Queries realizadas**

- `claude_websearch` · vetiver oil LMR IFF → 10 resultados
- `claude_websearch` · Chrysopogon zizanioides root essential oil GC-MS composition → 9 resultados
- `claude_websearch` · ISO 4716 vetiver oil → 10 resultados
- `claude_websearch` · vetiver oil safety data sheet CAS 8016-96-4 → 10 resultados
- `claude_websearch` · vetiver oil chemotype origin Haiti Java Bourbon → 9 resultados
- `claude_websearch` · vetiver oil use level perfumery → 9 resultados
- `claude_websearch` · Haiti vetiver oil GC-MS khusimol isovalencenol composition → 10 resultados
- `ncbi_pmc_api` · (vetiver[Title] OR "Chrysopogon zizanioides"[Title] OR "Vetiveria zizanioides"[Title]) AND (GC-MS OR "gas chromatography") AND oil → 12 resultados

**Fuentes encontradas:** 66 URLs distintas; 20 seleccionadas para descarga (MANUAL_RETRIEVAL_REQUIRED: 8, ENV_UNREACHABLE: 2, FETCHED: 9, ROBOTS_DISALLOWED: 1); 16 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://www.iff.com/scent/lmr-compendium/vetiver-concentrate-md-for-life/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-compendium/vetiver-heart/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-compendium/vetiver-oil-haiti/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-compendium/vetiver-oil-java/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://ir.iff.com/news-releases/news-release-details/iff-lmr-naturals-achieves-life-social-responsibility-0 — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: HTTPSConnectionPool(host='ir.i…)
- http://lmrnaturals.iff.com/en/scent/lmr-naturals/online-compendium/vetiver-oil-haiti — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: ('Connection aborted.', Connec…)
- https://www.tandfonline.com/doi/abs/10.1080/0972060X.2023.2264328 — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.carlroth.com/medias/SDB-6622-DE-EN.pdf?context=bWFzdGVyfHNlY3VyaXR5RGF0YXNoZWV0c3wyODIwNjN8YXBwbGljYXRpb24vcGRmfGFEWTJMMmc1T1M4NU1qQTJOelV3TlRjMk5qY3dMMU5FUWw4Mk5qSXlYMFJGWDBWT0xuQmtaZ3wwYWY3OWQ2YzQ5YmUwYzIzMGQxNjBjOWZiYWQzOGZmMWJjM2MwNGM1N2ViZDAwMTRmOTBhNWJiMzE0NzRkNWY0 — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://data.aromatics.com/products/484/download-sds — MANUAL_RETRIEVAL_REQUIRED (HTTP 429 (site refuses automated access; not bypassed))
- https://www.researchgate.net/profile/Br-Rajeswara-Rao/post/How-can-i-determine-the-best-extraction-method-for-specific-essential-oils/attachment/59d627fc79197b807798654c/AS:328208089141249@1455262314365/download/Vetiver+oil+composition.pdf — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.tandfonline.com/doi/abs/10.1080/10412905.2006.9699129 — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Evaluation of Vetiver Volatile Compound Production under Ae…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=8954624&rettype=xml) | peer-reviewed article; species found: chrysopogon zizanioides; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Vetiver, Vetiveria zizanioides (L.) Nash: Biotechnology, Bi…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=12114718&rettype=xml) | peer-reviewed article; species found: chrysopogon zizanioides; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Chrysopogon zizanioides (Vetiver) Essential Oil from Qatar …](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=12986586&rettype=xml) | peer-reviewed article; species found: chrysopogon zizanioides; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | OFFICIAL_MANUFACTURER | UNKNOWN_LICENSE | [Vetiver Oil Haiti / Givaudan](https://www.givaudan.com/fragrance-beauty/fragrance-ingredients-business/natural-ingredients/vetiver-oil-haiti) | trade/common name in title: 'vetiver oil'; CAS match ['8016-96-4']; official manufacturer domain (Givaudan); species match vetiveria zizanioides; reference for… |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [The Smelling Principle of Vetiver Oil, Unveiled by Chemical…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=7986879&rettype=xml) | peer-reviewed article; species found: chrysopogon zizanioides; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Vetiver Essential Oil in Cosmetics: What Is New?](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=5590077&rettype=xml) | peer-reviewed article; species found: chrysopogon zizanioides; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Chrysopogon zizanioides (Vetiver) Essential Oil from Qatar …](https://pubmed.ncbi.nlm.nih.gov/41829818/) | trade/common name in title: 'vetiver essential oil'; species match chrysopogon zizanioides; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Material Safety Data Sheet](https://cdn.accentuate.io/1800375107643/1592454388521/Vetiver---Material-Safety--Data-Sheet.pdf?v=0) | trade/common name in text: 'vetiver oil'; CAS match ['8016-96-4']; species match vetiveria zizanioides; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Page 1 ( 8 )](https://nikura.blob.core.windows.net/pdfs/Safety_Data_Sheet_Vetiver_Essential_Oil_EO-VET.pdf) | trade/common name in title: 'vetiver essential oil'; CAS match ['8016-96-4']; species match vetiveria zizanoides; reference for the natural type (not the schoo… |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Antibacterial, Antiparasitic, and Cytotoxic Activities of C…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=9415812&rettype=xml) | peer-reviewed article; species found: chrysopogon zizanioides; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [GC-MS analyses and bioactivities of essential oil obtained …](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=13061289&rettype=xml) | peer-reviewed article; species found: chrysopogon zizanioides; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [GC-MS analyses and bioactivities of essential oil obtained …](https://pubmed.ncbi.nlm.nih.gov/41958498/) | species match chrysopogon zizanioides; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://leerburg.com/pdf/scentOils/sds%20vetiver.pdf) | trade/common name in text: 'vetiver essential oil'; CAS match ['8016-96-4']; species match vetiveria zizanioides; reference for the natural type (not the schoo… |
| EXACT_CAS_ONLY | DISTRIBUTOR | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://www.vigon.com/product/vetiver-oil-haiti/?doc=MSDS%2F504190_vigon_sds_us_english.pdf&namee=VetiverOilHaitiSDS) | trade/common name in text: 'vetiver oil'; CAS match ['8016-96-4']; generic NCS CAS only |
| EXACT_CAS_ONLY | SECONDARY | UNKNOWN_LICENSE | [MATERIAL SAFETY DATA SHEET](https://www.oxfordlabfinechem.com/msds/(O-06483-244)%20OIL%20OF%20VETIVER%20Extra%20Pure.pdf) | CAS match ['8016-96-4']; generic NCS CAS only |
| EXACT_CAS_ONLY | SECONDARY | UNKNOWN_LICENSE | [Material Safety Data Sheet](https://www.indenta.com/imagehandler/image-handler.ashx?imagepath=product/msds/8016-96-4-2519.pdf) | trade/common name in text: 'vetiver oil'; CAS match ['8016-96-4']; generic NCS CAS only |

**Confianza de identidad:** LIKELY_MATCH (score 0.70)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 8016-96-4 |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.oxfordlabfinechem.com |
| cas | 8016-96-4 |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.indenta.com |
| cas | 8016-96-4 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| cas | 84238-29-9 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | nikura.blob.core.windows.net |
| cas | 8016-96-4 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| vapour_pressure | 1.520000 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| density | 0.960 – 1.012 @ 20°C | 0.986 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.oxfordlabfinechem.com |
| density | 0.960-1.012 | 0.986 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.oxfordlabfinechem.com |
| density | 0.9600 - 1.0050 | 0.9825 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| density | 0.9600-1.0050 | 0.9825 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| density | 0.980 - 1.015 @ 20°C. | 0.9975 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | leerburg.com |
| density | 0.980-1.015 | 0.9975 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | leerburg.com |
| refractive_index | 1.510 - 1.530 @ 20°C | 1.52 nD | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.oxfordlabfinechem.com |
| refractive_index | 1.510-1.530 | 1.52 nD | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.oxfordlabfinechem.com |
| flash_point | 100 |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.oxfordlabfinechem.com |
| flash_point | > 104 °C | 104.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| flash_point | >104 C | 104.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| boiling_point | 276 C | 276.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| physical_state | Viscous liquid, brown orange to red. |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.oxfordlabfinechem.com |
| physical_state | liquid |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.indenta.com |
| physical_state | Brown to reddish brown liquid. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| physical_state | Amber brown to reddish brown colored, slightly viscous liquid. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | leerburg.com |
| solubility | Insoluble. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | leerburg.com |
| odour_description | Characteristic sweet woody herbaceous. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| odour_description | Deep, rich, slightly sweet, resinous, earthy odour. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | leerburg.com |
| product_code | V1219 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| product_code | 10ml: 5060683141082, 2x10ml: 5060683141099, 3x10ml: |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| botanical_name | chrysopogon zizanioides |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | chrysopogon zizanioides |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | chrysopogon zizanioides |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | vetiveria zizanioides |  | MANUFACTURER | LIKELY_MATCH | VALID | www.givaudan.com |
| botanical_name | vetiveria zizanoides |  | MANUFACTURER | LIKELY_MATCH | VALID | www.givaudan.com |
| botanical_name | chrysopogon zizanioides |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | chrysopogon zizanioides |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | chrysopogon zizanioides |  | PUBLISHED | LIKELY_MATCH | VALID | pubmed.ncbi.nlm.nih.gov |
| botanical_name | vetiveria zizanioides |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| botanical_name | vetiveria zizanoides |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| botanical_name | chrysopogon zizanioides |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | chrysopogon zizanioides |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | chrysopogon zizanioides |  | PUBLISHED | LIKELY_MATCH | VALID | pubmed.ncbi.nlm.nih.gov |
| botanical_name | vetiveria zizanioides |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | leerburg.com |
| h_statement | H317 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| h_statement | H304 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| h_statement | H315 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| h_statement | H317 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| h_statement | H411 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| signal_word | Danger |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| sds_product_name | OIL OF VETIVER Extra Pure |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.oxfordlabfinechem.com |
| sds_product_name | Vetiver oil |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.indenta.com |
| sds_product_name | s: |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| sds_product_name | Product identifier: Vetiveria Zizanoides; CAS: 8016-96-4 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| sds_product_name | Chemical Name/Synonyms: VETIVER ESSENTIAL OIL |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | leerburg.com |
| sds_component_cas | 8016-96-4 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| sds_component_cas | 8016-96-4 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| sds_component_cas | 15764-04-2 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| sds_component_cas | 18444-79-6 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | nikura.blob.core.windows.net |
| sds_component_cas | 8016-96-4 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | leerburg.com |
| sds_component_cas | 84238-29-9 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | leerburg.com |
| storage | Store in tightly-closed, original container in a dry, cool and well-v… |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.oxfordlabfinechem.com |
| storage | stored in a separate safety storage cabinet or room. |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.indenta.com |
_… 16 claims más en data/staging.sqlite_

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** vapour_pressure=1.520000 (SECONDARY_REFERENCE SDS, NEEDS_REVIEW)
**SDS/CLP (por SDS, sin mezclar):** cdn.accentuate.io: H317 · nikura.blob.core.windows.net: Danger, H304, H315, H317, H411

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `cas`: source CAS not in master CAS set — valores: 84238-29-9 [SECONDARY]; 8016-96-4 [SECONDARY]; 8016-96-4 [SECONDARY]; 8016-96-4 [SECONDARY]; 8016-96-4 [SECONDARY]; 8016-96-4 [MASTER]
- `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] — valores: H317 [SECONDARY]; H304 [SECONDARY]; H315 [SECONDARY]; H317 [SECONDARY]; H411 [SECONDARY]

**Cambios propuestos:** 5 (NEEDS_REVIEW: 5)

- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H317
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H304, H315, H317, H411
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=khusimol, Sample relative peak area %=0.6
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=beta-vetivone, Sample relative peak area %=2.2
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/lmr-compendium/vetiver-concentrate-md-for-life/): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Resolver conflicto en `cas`: source CAS not in master CAS set
- Resolver conflicto en `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only]
- La composición GC-MS publicada es REFERENCE_COMPOSITION (muestras de investigación), nunca la botella ISIPCA; falta CoA/especificación del lote.

---

## N-0697 — ROSE OIL TURKISH LMR

*Grupo piloto:* NATURAL · *Qué prueba:* natural GC-MS, ISO 9842, botanical identity
*Estado final:* **NEEDS_REVIEW** — 4 conflicts; 13 changes need review
*Master antes:* tier `C_CLOSE_OR_AMBIGUOUS_REFERENCE`, CAS `8007-01-0`, readiness 36 (NOT_READY)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 36 (NOT_READY); si se aprueban también los NEEDS_REVIEW → 38 (NOT_READY)

**Queries realizadas**

- `claude_websearch` · rose oil Turkish LMR IFF → 10 resultados
- `claude_websearch` · Rosa damascena flower essential oil GC-MS composition Turkey → 9 resultados
- `claude_websearch` · ISO 9842 rose oil Rosa x damascena → 10 resultados
- `claude_websearch` · rose oil Turkey safety data sheet CAS 8007-01-0 → 10 resultados
- `claude_websearch` · Turkish rose oil Isparta origin citronellol geraniol ratio Bulgarian comparison → 9 resultados
- `claude_websearch` · rose oil use level perfumery IFRA methyl eugenol → 9 resultados
- `ncbi_pmc_api` · ("Rosa damascena"[Title] OR "rose oil"[Title]) AND (GC-MS OR "gas chromatography") AND (oil OR otto) → 12 resultados

**Fuentes encontradas:** 53 URLs distintas; 29 seleccionadas para descarga (FETCHED: 12, MANUAL_RETRIEVAL_REQUIRED: 8, ROBOTS_DISALLOWED: 8, ENV_UNREACHABLE: 1); 17 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://www.iff.com/scent/lmr-compendium/rose-abs-md-turkey-for-life/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-compendium/rose-essential-for-life/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-compendium/rose-essential-low-me-for-life/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-compendium/rose-ultimate-extract-for-life/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.thegoodscentscompany.com/data/es1050111.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/es1050111.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://www.sciencedirect.com/science/article/abs/pii/S030881462100501X — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.sciencedirect.com/science/article/abs/pii/S092666901730393X — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.sciencedirect.com/science/article/pii/S2225411015000954 — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/rosa-damascena — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://scijournals.onlinelibrary.wiley.com/doi/abs/10.1002/jsfa.2740640408 — MANUAL_RETRIEVAL_REQUIRED (HTTP 403 (site refuses automated access; not bypassed))
- https://www.chemicalbook.com/ChemicalProductProperty_EN_CB6167644.htm — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 429 (site refuses automated access; not bypassed))
- https://www.chemicalbook.com/ProductChemicalPropertiescb6167644_EN.htm — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 429 (site refuses automated access; not bypassed))
- https://www.sigmaaldrich.com/catalog/product/aldrich/w523704?lang=en&region=US — ENV_UNREACHABLE (robots.txt unreachable: HTTPSConnectionPool(host='www.sigmaaldrich.com', port=443): Read …)
- https://www.spectrumchemical.com/cas/8007-01-0 — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.researchgate.net/publication/233853035_Turkish_rose_oil_Recent_results — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.ouddict.com/threads/warning-about-rose-oils.2773/ — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.sciencedirect.com/science/article/abs/pii/S0962456203000067 — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Chemical Composition, Biological Activity, and Application …](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=11592901&rettype=xml) | peer-reviewed article; species found: rosa damascena; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Phenotyping floral traits and essential oil profiling revea…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=10198992&rettype=xml) | peer-reviewed article; species found: rosa damascena; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Determination of Major, Minor and Chiral Components as Qual…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=9921129&rettype=xml) | peer-reviewed article; species found: rosa damascena; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://ultrainternational.com/wp-content/uploads/2023/08/SDS-ROSE-OIL.pdf) | trade/common name in text: 'rose oil'; CAS match ['8007-01-0']; species match rosa x damascena; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Chemical Composition, Antifungal Activity, and Plant-Protec…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=12030332&rettype=xml) | peer-reviewed article; species found: rosa damascena; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Rose Oil, Isparta – Fraterworks](https://fraterworks.com/products/rose-oil-isparta) | trade/common name in title: 'rose oil'; CAS match ['8007-01-0']; expected manufacturer 'LMR Naturals (IFF)' mentioned; species match rosa x damascena; referenc… |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Rosa × damascena Herrm. From Azaran region, Kashan: rich in…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=11234773&rettype=xml) | peer-reviewed article; species found: rosa damascena; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | SECONDARY_DB | PRODUCTION_SAFE_WITH_ATTRIBUTION | [Rose oil - Wikipedia](https://en.wikipedia.org/wiki/Rose_oil) | trade/common name in title: 'rose oil'; species match rosa damascena; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Rose Otto, Turkey EO / Eden Botanicals](https://www.edenbotanicals.com/rose-otto-turkey-886.html) | trade/common name in title: 'rose otto'; CAS match ['8007-01-0']; species match rosa damascena; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Rose Otto Turkish Organic Essential Oil / Amrita Aromathera…](https://www.amrita.net/rose-otto-turkish-organic-essential-oil/) | trade/common name in title: 'rose otto'; species match rosa damascena; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Rose Oil SDS (CAS 8007-01-0) / Download MSDS PDF & Safety D…](https://www.chemblink.com/en/MSDS/8007-01-0MSDS.htm) | trade/common name in title: 'rose oil'; CAS match ['8007-01-0']; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [CAS No.8007-01-0,Rose oil Suppliers](https://www.lookchem.com/cas-800/8007-01-0.html) | trade/common name in title: 'rose oil'; CAS match ['8007-01-0']; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Erçetin Rose Oil - IFF Harvests Turkish Rose](https://www.ercetin.com/video-play-iff-harvests-turkish-rose.html) | trade/common name in title: 'rose oil'; expected manufacturer 'LMR Naturals (IFF)' mentioned; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [ROSE OIL TURKISH LMR – Fine Fragrances Pvt Ltd](https://finefrag.com/product/rose-oil-turkish-lmr/) | trade/common name in title: 'rose oil turkish'; expected manufacturer 'LMR Naturals (IFF)' mentioned; reference for the natural type (not the school bottle) |
| EXACT_CAS_ONLY | SECONDARY | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://finefrag.com/wp-content/uploads/2020/06/ROSE-OIL-TURKISH-LMR_00181102_GHS_SDS_28May2020_482142.pdf) | trade/common name in text: 'rose oil turkish'; CAS match ['8007-01-0']; expected manufacturer 'LMR Naturals (IFF)' mentioned; generic NCS CAS only; SDS issued … |

**Fuentes rechazadas:** 2

- Methyl Eugenol | — no name, species or CAS match
- ABC Herbalgram Website — no name, species or CAS match

**Confianza de identidad:** LIKELY_MATCH (score 0.70)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 8007-01-0 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| cas | 90106-38-0 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | ultrainternational.com |
| cas | 8007-01-0 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
| cas | 90106-38-0 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | CONFLICT | finefrag.com |
| cas | 8007-01-0 |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| cas | 8007-01-0 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemblink.com |
| cas | 8007-01-0 |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| cas | 8007-01-0 |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.lookchem.com |
| vapour_pressure | 0.13 hPa | 13.0 Pa | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
| tenacity | Lasts > 170 hours on a smelling strip | 170.0 hours | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| density | 0.848 - 0.880 @20°C | 0.864 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | ultrainternational.com |
| density | 0.848-0.880 | 0.864 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | ultrainternational.com |
| density | 0.964 g/mL at 25 °C(lit.) | 0.964 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE | LIKELY_MATCH | CONFLICT | www.lookchem.com |
| refractive_index | 1.452 - 1.470 @20°C | 1.461 nD | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| refractive_index | 1.452-1.470 | 1.461 nD | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| flash_point | >93°C | 93.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | ultrainternational.com |
| flash_point | >93 C | 93.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | ultrainternational.com |
| flash_point | 45 °C | 45.0 C | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | VALID_DISPUTED | finefrag.com |
| flash_point | 45 C | 45.0 C | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | VALID_DISPUTED | finefrag.com |
| flash_point | 150 °F | 65.6 C | SECONDARY_REFERENCE | LIKELY_MATCH | CONFLICT | www.lookchem.com |
| flash_point | 150 F | 65.6 C | SECONDARY_REFERENCE | LIKELY_MATCH | CONFLICT | www.lookchem.com |
| boiling_point | 176 °C | 176.0 C | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.lookchem.com |
| physical_state | Liquid |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| physical_state | liquid |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
| physical_state | Clear liquid, solidifies in cool temperatures |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| physical_state | Very pale yellowish green, transparent, slightly viscous, mobile liqu… |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| physical_state | Colorless or yellow, thick volatile oil, with peculiar rose smell and… |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.lookchem.com |
| physical_state | reddish liquid Storage:2-8°C Package:25kg/barrel Application:Pharmace… |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.lookchem.com |
| physical_state | liquid Storage:Store the container tightly closed in a dry, cool and … |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.lookchem.com |
| physical_state | solid or liquid Storage:in sealed air resistant place Package:drum an… |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.lookchem.com |
| solubility | Soluble in ethanol and the majority of volatile oil, very slightly so… |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.lookchem.com |
| odour_description | Floral, Sweet, Spicy, Wine and rose |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| product_code | UL3000292 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| product_code | Choose an option FG0027 |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | finefrag.com |
| product_code | FG0027 |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | finefrag.com |
| ec_number | 290-260-3 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| ec_number | 290-260-3 |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.lookchem.com |
| botanical_name | rosa damascena |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | rosa damascena |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | rosa damascena |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | rosa x damascena |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| botanical_name | rosa damascena |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | rosa x damascena |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| botanical_name | rosa damascena |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | rosa damascena |  | SECONDARY_REFERENCE | LIKELY_MATCH | VALID | en.wikipedia.org |
| botanical_name | rosa centifolia |  | SECONDARY_REFERENCE | LIKELY_MATCH | VALID | en.wikipedia.org |
| botanical_name | cymbopogon |  | SECONDARY_REFERENCE | LIKELY_MATCH | VALID | en.wikipedia.org |
| botanical_name | Rosa x damascena Mill. |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| botanical_name | Rosa Damascena (Rose) Flower Oil |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| botanical_name | rosa damascena |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| botanical_name | rosa x damascena |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| botanical_name | rosa damascena |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.amrita.net |
| plant_part | Blossom |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.amrita.net |
| extraction_method | Hydrodistilled |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| extraction_method | Steam Distilled |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.amrita.net |
| origin | Turkey |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.amrita.net |
| iso_standard | ISO 9842 |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| iso_standard | ISO 9842:2003 |  | SECONDARY_REFERENCE | LIKELY_MATCH | VALID | en.wikipedia.org |
| iso_standard | ISO 9001 |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.lookchem.com |
| iso_standard | ISO 14001 |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.lookchem.com |
_… 58 claims más en data/staging.sqlite_

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** vapour_pressure=0.13 hPa (MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF), NEEDS_REVIEW); tenacity=Lasts > 170 hours on a smelli… (RETAILER (SECONDARY CLAIM), VALID)
**SDS/CLP (por SDS, sin mezclar):** finefrag.com: Danger, H226, H303, H315, H317, H318, H341, H351, H401, H412 · ultrainternational.com: Aquatic Acute 2, Aquatic Chronic 2, Asp. Tox. 1, Carc. 2, Danger, H304, H313, H315, H317, H318, H341, H351, H401, H411, Muta. 2, Skin Irrit. 2, Skin Sens. 1

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `density`: density: independent sources disagree beyond tolerance ('abs', 0.012) — valores: 0.848 - 0.880 @20°C [SECONDARY]; 0.848-0.880 [SECONDARY]; 0.964 g/mL at 25 °C(lit.) [SECONDARY]
- `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only] — valores: >93°C [SECONDARY]; >93 C [SECONDARY]; 45 °C [SECONDARY]; 45 C [SECONDARY]; 150 °F [SECONDARY]; 150 F [SECONDARY]
- `cas`: source CAS not in master CAS set — valores: 90106-38-0 [SECONDARY]; 90106-38-0 [SECONDARY]; 8007-01-0 [SECONDARY]; 8007-01-0 [SECONDARY]; 8007-01-0 [RETAILER]; 8007-01-0 [SECONDARY]; 8007-01-0 [SECONDARY]; 8007-01-0 [SECONDARY]
- `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] — valores: H313 [SECONDARY]; H315 [SECONDARY]; H317 [SECONDARY]; H318 [SECONDARY]; H341 [SECONDARY]; H351 [SECONDARY]; H304 [SECONDARY]; H401 [SECONDARY]

**Cambios propuestos:** 14 (NEEDS_REVIEW: 14)

- `NEEDS_REVIEW` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=>170.0, unit=hours
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes=Aquatic Acute 2; Aquatic Chronic 2; Asp. Tox. 1; Carc. 2; Muta. 2; Skin Irrit. 2; Skin Sens. 1 | H: H304, H313, H315, H317, …
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H226, H303, H315, H317, H318, H341, H351, H401, H412
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalool, Sample relative peak area %=0.38-10.355
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=citronellol, Sample relative peak area %=15.279-44.75
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=geraniol, Sample relative peak area %=15.63-27.75
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=eugenol, Sample relative peak area %=0.2-19.302
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=heneicosane, Sample relative peak area %=4.96-40.848
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=citronellol, Sample relative peak area %=7.37
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=geraniol, Sample relative peak area %=1.58
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=eugenol, Sample relative peak area %=0.29
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=nonadecane, Sample relative peak area %=3.7
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=heneicosane, Sample relative peak area %=2.27
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/lmr-compendium/rose-abs-md-turkey-for-life/): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Resolver conflicto en `density`: density: independent sources disagree beyond tolerance ('abs', 0.012)
- Resolver conflicto en `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only]
- Resolver conflicto en `cas`: source CAS not in master CAS set
- Resolver conflicto en `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only]
- La composición GC-MS publicada es REFERENCE_COMPOSITION (muestras de investigación), nunca la botella ISIPCA; falta CoA/especificación del lote.

---

## N-0623 — SAGE CLARY OIL FRENCH LMR

*Grupo piloto:* NATURAL · *Qué prueba:* natural GC-MS, ISO 7609, chemotype/origin
*Estado final:* **NEEDS_REVIEW** — 1 conflicts; 15 changes need review
*Master antes:* tier `C_GENERIC_NATURAL_REFERENCE`, CAS `8016-63-5`, readiness 36 (NOT_READY)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 36 (NOT_READY); si se aprueban también los NEEDS_REVIEW → 36 (NOT_READY)

**Queries realizadas**

- `claude_websearch` · clary sage oil French LMR IFF → 10 resultados
- `claude_websearch` · Salvia sclarea essential oil GC-MS composition linalyl acetate linalool → 10 resultados
- `claude_websearch` · ISO 7609 clary sage oil → 10 resultados
- `claude_websearch` · clary sage oil safety data sheet CAS 8016-63-5 → 10 resultados
- `claude_websearch` · clary sage oil France origin chemotype sclareol Russia Bulgaria → 9 resultados
- `claude_websearch` · clary sage oil use level perfumery → 9 resultados
- `claude_websearch` · "ISO 7609" essential oil clary sage Salvia sclarea → 9 resultados
- `ncbi_pmc_api` · ("Salvia sclarea"[Title] OR "clary sage"[Title]) AND (GC-MS OR "gas chromatography") AND "essential oil" → 12 resultados

**Fuentes encontradas:** 61 URLs distintas; 25 seleccionadas para descarga (FETCHED: 5, MANUAL_RETRIEVAL_REQUIRED: 9, ENV_UNREACHABLE: 3, ROBOTS_DISALLOWED: 8); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://www.iff.com/scent/lmr-compendium/sage-clary-absolute-france/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-compendium/sage-clary-oil-france/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-compendium/sage-clary-oil-green-france/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- http://lmrnaturals.iff.com/en/site-services/flavor-online-compendium-iframe/clary-sage-oil — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: ('Connection aborted.', Connec…)
- http://lmrnaturals.iff.com/en/site-services/lmr-naturals-online-compendium/sage-clary-oil-france — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: ('Connection aborted.', Connec…)
- https://www.thegoodscentscompany.com/data/es1018512.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/es1018512.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://www.sciencedirect.com/science/article/pii/S2214662826000265 — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.tandfonline.com/doi/abs/10.1080/10412905.2010.9700406 — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.tandfonline.com/doi/full/10.1080/14786419.2019.1593168 — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.chemicalbook.com/ChemicalProductProperty_EN_CB9340183.htm — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 429 (site refuses automated access; not bypassed))
- https://www.thegoodscentscompany.com/data/es1101491.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/es1101491.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://www.thegoodscentscompany.com/data/es1585161.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/es1585161.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://www.thegoodscentscompany.com/data/es1585171.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/es1585171.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://www.ulprospector.com/en/na/PersonalCare/Detail/2357/647759/Clary-Sage-Oil — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://cdn.planttherapy.com/sds/clary_sage_eo.pdf — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.chemicalbook.com/ProductChemicalPropertiesCB9340183_EN.htm — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 429 (site refuses automated access; not bypassed))
- https://dam.hollandandbarrettimages.co.uk/uk_ie/sds_-clarysageessentialoil.pdf — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://ultranl.com/wp-content/uploads/SDS-CLARY-SAGE-OIL-FRANCE.pdf — ENV_UNREACHABLE (robots.txt unreachable: HTTPSConnectionPool(host='ultranl.com', port=443): Max retries ex…)
- https://www.aroma-zone.com/en/guide/organic-clary-sage-essential-oil — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.ewg.org/cleaners/substances/5290-SALVIASCLAREACLARYSAGEOIL/ — MANUAL_RETRIEVAL_REQUIRED (HTTP 403 (site refuses automated access; not bypassed))

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Salvia sclarea Essential Oil Chemical Composition and Biolo…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=10049179&rettype=xml) | peer-reviewed article; species found: salvia sclarea; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Laurus nobilis, Salvia sclarea and Salvia officinalis Essen…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=8067454&rettype=xml) | peer-reviewed article; species found: salvia sclarea; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Salvia officinalis L. and Salvia sclarea Essential Oils: Ch…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=10574192&rettype=xml) | peer-reviewed article; species found: salvia sclarea; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Safety and efficacy of a feed additive consisting of an ess…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=11561422&rettype=xml) | peer-reviewed article; species found: salvia sclarea; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Mechanistic insights into clary sage oils role in wound hea…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=12394166&rettype=xml) | peer-reviewed article; species found: salvia sclarea; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Material Safety Data Sheet](https://cdn.accentuate.io/1871053684795/1619828099392/Clary-Sage---Material-Safety--Data-Sheet.pdf?v=0) | trade/common name in text: 'clary sage oil'; CAS match ['8016-63-5']; species match salvia sclarea; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Chemical Composition, Antioxidant and Anti-Inflammatory Act…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=8434190&rettype=xml) | peer-reviewed article; species found: salvia sclarea; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Supercritical Fluid Extraction of Essential Oil and Sclareo…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=10179952&rettype=xml) | peer-reviewed article; species found: salvia sclarea; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Combination of Analytical and Statistical Methods in Order …](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=8586929&rettype=xml) | peer-reviewed article; species found: salvia sclarea; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Study of the genetic and phenotypic variation among wild an…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=8294528&rettype=xml) | peer-reviewed article; species found: salvia sclarea; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Clary Sage Essential Oil - Salvia Sclarea - France - LMR – …](https://bulkaroma.com/products/clary-sage-essential-oil-salvia-sclarea-france-lmr) | trade/common name in title: 'clary sage essential oil'; CAS match ['8016-63-5']; expected manufacturer 'LMR Naturals (IFF)' mentioned; species match salvia scl… |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [www.newdirectionsaromatics.com](https://docs.newdirectionsaromatics.com/msds/SDS_ClarySageOrganicEO.pdf) | CAS match ['8016-63-5']; species match salvia sclarea; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [LMR – Bulkaroma](https://bulkaroma.com/en-us/collections/vendors?q=LMR) | trade/common name in text: 'clary sage essential oil'; CAS match ['8016-63-5']; expected manufacturer 'LMR Naturals (IFF)' mentioned; species match salvia scla… |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [CAS 8016-63-5 Clary sage oil - Alfa Chemistry](https://www.alfa-chemistry.com/cas_8016-63-5.htm) | trade/common name in title: 'clary sage oil'; CAS match ['8016-63-5']; reference for the natural type (not the school bottle) |

**Confianza de identidad:** LIKELY_MATCH (score 0.70)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 8016-63-5 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| cas | 8016-63-5 |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.alfa-chemistry.com |
| density | 0.885 to 0.945 @ 20 °C | 0.915 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| density | 0.885-0.945 | 0.915 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| refractive_index | 1.456 to 1.515@ 20°C | 1.4855 nD | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| refractive_index | 1.456-1.515 | 1.4855 nD | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| flash_point | 79°C | 79.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| flash_point | 79 C | 79.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| physical_state | Colorless to brown-yellow liquid |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| solubility | Soluble in alcohol and oils. Insoluble in water. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| odour_description | Sweet, herbaceous, Linalyl-acetate like with tobacco-like complexion |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| product_code | 512375-14 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| botanical_name | salvia sclarea |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | salvia sclarea |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | salvia sclarea |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | salvia sclarea |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | salvia sclarea |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | salvia sclarea |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| botanical_name | salvia sclarea |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | salvia sclarea |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | salvia sclarea |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | salvia sclarea |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | salvia sclarea |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | bulkaroma.com |
| botanical_name | Salvia Sclarea L. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| botanical_name | Salvia Sclarea Flower Oil |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| botanical_name | salvia sclarea |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| botanical_name | salvia sclarea |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | bulkaroma.com |
| origin | France/Egypt |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| h_statement | H227 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| h_statement | H315 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| h_statement | H315 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| h_statement | H317 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| h_statement | H319 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| h_statement | H402 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| h_statement | H412 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| signal_word | Warning |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| sds_product_name | s: |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| sds_product_name | Clary Sage Organic Essential Oil |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| sds_component_cas | 8016-63-5 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| sds_component_cas | 115-95-7 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| sds_component_cas | 78-70-6 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| sds_component_cas | 5392-40-5 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| sds_component_cas | 105-87-3 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| sds_component_cas | 106-24-1 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| sds_component_cas | 80-56-8 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| sds_component_cas | 3779-61-1 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| sds_component_cas | 3338-55-4 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| sds_component_cas | 5989-27-5 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| sds_component_cas | 127-91-3 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| stability_text | Stable under recommended storage conditions. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | cdn.accentuate.io |
| stability_text | Stable at ambient temperatures. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | docs.newdirectionsaromatics.com |
| gcms_study | Salvia sclarea Essential Oil Chemical Composition and Biological Acti… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Laurus nobilis, Salvia sclarea and Salvia officinalis Essential Oils … |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Salvia officinalis L. and Salvia sclarea Essential Oils: Chemical Com… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Safety and efficacy of a feed additive consisting of an essential oil… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Mechanistic insights into clary sage oils role in wound healing: targ… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Chemical Composition, Antioxidant and Anti-Inflammatory Activities of… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Supercritical Fluid Extraction of Essential Oil and Sclareol from a C… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Combination of Analytical and Statistical Methods in Order to Optimiz… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Study of the genetic and phenotypic variation among wild and cultivat… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
_… 13 claims más en data/staging.sqlite_

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** ninguna encontrada
**SDS/CLP (por SDS, sin mezclar):** cdn.accentuate.io: H227, H315, Warning · docs.newdirectionsaromatics.com: H315, H317, H319, H402, H412

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] — valores: H227 [SECONDARY]; H315 [SECONDARY]; H315 [SECONDARY]; H317 [SECONDARY]; H319 [SECONDARY]; H402 [SECONDARY]; H412 [SECONDARY]

**Cambios propuestos:** 16 (NEEDS_REVIEW: 16)

- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H227, H315
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H315, H317, H319, H402, H412
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalool, Sample relative peak area %=0.3-11.3
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalyl acetate, Sample relative peak area %=59.3
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=geranyl acetate, Sample relative peak area %=2.5
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=beta-caryophyllene, Sample relative peak area %=1.2-3.7
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=germacrene d, Sample relative peak area %=0.3-10.5
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=geranyl acetate, Sample relative peak area %=1.04
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=neryl acetate, Sample relative peak area %=0.77
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=sclareol, Sample relative peak area %=0.51
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalool, Sample relative peak area %=9.1
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=alpha-terpineol, Sample relative peak area %=10.1
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalyl acetate, Sample relative peak area %=2.5-13.4
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=caryophyllene, Sample relative peak area %=3.2
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=sclareol, Sample relative peak area %=25.3
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/lmr-compendium/sage-clary-absolute-france/): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Resolver conflicto en `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only]
- La composición GC-MS publicada es REFERENCE_COMPOSITION (muestras de investigación), nunca la botella ISIPCA; falta CoA/especificación del lote.

---

## N-0632 — CARDAMOM OIL EI LMR

*Grupo piloto:* NATURAL · *Qué prueba:* natural GC-MS, ISO 4733, EI origin code
*Estado final:* **NEEDS_REVIEW** — 3 conflicts; 13 changes need review
*Master antes:* tier `C_GENERIC_NATURAL_REFERENCE`, CAS `8000-66-6`, readiness 36 (NOT_READY)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 36 (NOT_READY); si se aprueban también los NEEDS_REVIEW → 36 (NOT_READY)

**Queries realizadas**

- `claude_websearch` · cardamom oil LMR IFF → 9 resultados
- `claude_websearch` · Elettaria cardamomum seed essential oil GC-MS composition 1,8-cineole alpha-terpinyl acetate → 9 resultados
- `claude_websearch` · ISO 4733 cardamom oil → 10 resultados
- `claude_websearch` · cardamom oil safety data sheet CAS 8000-66-6 → 10 resultados
- `claude_websearch` · cardamom oil origin Guatemala India chemotype composition comparison → 9 resultados
- `claude_websearch` · cardamom oil use level perfumery → 9 resultados
- `claude_websearch` · "CARDAMOM OIL EI" LMR → 10 resultados
- `claude_websearch` · cardamom oil East Indian LMR Naturals India → 9 resultados
- `ncbi_pmc_api` · ("Elettaria cardamomum"[Title] OR cardamom[Title]) AND (GC-MS OR "gas chromatography") AND "essential oil" → 12 resultados

**Fuentes encontradas:** 67 URLs distintas; 17 seleccionadas para descarga (FETCHED: 9, MANUAL_RETRIEVAL_REQUIRED: 7, ENV_UNREACHABLE: 1); 16 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://www.iff.com/scent/lmr-compendium/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-compendium/cardamom-guatemala-co2-extract/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-compendium/cardamom-oil-guatemala/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-naturals/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.tandfonline.com/doi/full/10.1080/16583655.2021.2002550 — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2019.5721 — MANUAL_RETRIEVAL_REQUIRED (HTTP 403 (site refuses automated access; not bypassed))
- https://pellwall.com/products/cardamom-oil-albert-vieille-1 — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: HTTPSConnectionPool(host='pell…)
- https://www.iff.com/scent/lmr-compendium/elemi-oil/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Cardamom, Cumin, and Dill Weed Essential Oils: Chemical Com…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=6152346&rettype=xml) | peer-reviewed article; species found: elettaria cardamomum; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Changes in cardamom (Elettaria cardamomum) fatty acid compo…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=12329038&rettype=xml) | peer-reviewed article; species found: elettaria cardamomum; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Fumigant toxicity and oviposition deterrency of the essenti…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=3281396&rettype=xml) | peer-reviewed article; species found: elettaria cardamomum; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | OFFICIAL_MANUFACTURER | UNKNOWN_LICENSE | [Cardamom Oil Guatemala / Givaudan](https://www.givaudan.com/fragrance-beauty/fragrance-ingredients-business/natural-ingredients/cardamom-oil-guatemala) | trade/common name in title: 'cardamom oil'; CAS match ['8000-66-6']; official manufacturer domain (Givaudan); species match elettaria cardamomum; reference for… |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Cardamom Essential Oil /](https://www.perfumersworld.com/view.php?pro_id=7SC00084) | trade/common name in title: 'cardamom essential oil'; CAS match ['8000-66-6']; species match elettaria cardamomum; reference for the natural type (not the scho… |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [NHR ORGANIC OILS](https://www.nhrorganicoils.com/uploads/20221122161304e_Cardamom_SDS.pdf) | trade/common name in text: 'cardamom essential oil'; CAS match ['8000-66-6']; species match elettaria cardamomum; reference for the natural type (not the schoo… |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [SAFETY DATA SHEET](http://ultrainternational.com/wp-content/uploads/2023/08/SDS-CARDAMOM-OIL.pdf) | trade/common name in text: 'cardamom oil'; CAS match ['8000-66-6']; species match elettaria cardamomum; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Cardamom Oil — Natural Ingredient for Perfumery — Scentspir…](https://www.scentspiracy.com/fragrance-ingredients/p/cardamom-oil) | trade/common name in title: 'cardamom oil'; CAS match ['8000-66-6']; species match elettaria cardamomum; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Antiparasitic effects of Elettaria cardamomum L. essential …](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=9073046&rettype=xml) | peer-reviewed article; species found: elettaria cardamomum; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Antioxidant Activity and GC-MS Profile of Cardamom (Elettar…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=9920946&rettype=xml) | peer-reviewed article; species found: elettaria cardamomum; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Safety and efficacy of an essential oil from Elettaria card…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=7009127&rettype=xml) | peer-reviewed article; species found: elettaria cardamomum; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Effects of Essential Oils of Elettaria cardamomum Grown in …](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=8123808&rettype=xml) | peer-reviewed article; species found: elettaria cardamomum; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Cardamom Oil SDS (CAS 8000-66-6) / Download MSDS PDF & Safe…](https://www.chemblink.com/MSDS/8000-66-6_MSDS.htm) | trade/common name in title: 'cardamom oil'; CAS match ['8000-66-6']; reference for the natural type (not the school bottle) |
| EXACT_CAS_ONLY | DISTRIBUTOR | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://www.vigon.com/product/cardamom-oil-guatemala/?doc=MSDS%2F504064_vigon_sds_us_english.pdf&namee=CardamomOilGuatemalaSDS) | trade/common name in text: 'cardamom oil'; CAS match ['8000-66-6']; generic NCS CAS only |
| EXACT_CAS_ONLY | SECONDARY | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://finefrag.com/wp-content/uploads/2020/06/CARDAMOM-OIL-GUATEMALA-LMR_00032885_GHS_SDS_28May2020_482080.pdf) | trade/common name in text: 'cardamom oil'; CAS match ['8000-66-6']; expected manufacturer 'LMR Naturals (IFF)' mentioned; generic NCS CAS only; SDS issued by I… |
| EXACT_CAS_ONLY | SECONDARY | UNKNOWN_LICENSE | [Oils, cardamom MSDS CasNo.8000-66-6](https://www.lookchem.com/msds/36131/8000-66-6_Oils,%20cardamom.html) | trade/common name in text: 'cardamom oil'; CAS match ['8000-66-6']; generic NCS CAS only |

**Confianza de identidad:** LIKELY_MATCH (score 0.70)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 85940-32-5 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | CONFLICT | finefrag.com |
| cas | 8000-66-6 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
| cas | 8000-66-6 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| cas | 85940-32-5 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | ultrainternational.com |
| cas | 8000-66-6 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.chemblink.com |
| cas | 8000-66-6 |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.lookchem.com |
| cas | 93062-62-5 |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | CONFLICT | www.lookchem.com |
| vapour_pressure | 0.13 hPa | 13.0 Pa | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
| density | 0.920 - 0.940 @25°C | 0.93 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| density | 0.920-0.940 | 0.93 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| density | >1 (air=1) |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.lookchem.com |
| refractive_index | 1.460 - 1.467 @20°C | 1.4635 nD | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| refractive_index | 1.460-1.467 | 1.4635 nD | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| flash_point | 57 C | 57.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | CONFLICT | www.nhrorganicoils.com |
| flash_point | 65 °C | 65.0 C | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | VALID_DISPUTED | finefrag.com |
| flash_point | 65 C | 65.0 C | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | VALID_DISPUTED | finefrag.com |
| flash_point | 59°C | 59.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| flash_point | 59 C | 59.0 C | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| flash_point | 57oC |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.lookchem.com |
| physical_state | liquid |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
| physical_state | Liquid |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| physical_state | Clear oil |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.lookchem.com |
| odour_description | warm spicy balsam woody odor |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| odour_description | Sweet, warm, spicy, typical |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.lookchem.com |
| product_code | UL3000121 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| ec_number | 288-922-1 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| botanical_name | elettaria cardamomum |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | elettaria cardamomum |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | elettaria cardamomum |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | elettaria cardamomum |  | MANUFACTURER | LIKELY_MATCH | VALID | www.givaudan.com |
| botanical_name | elettaria cardamomum |  | DISTRIBUTOR_SPEC | LIKELY_MATCH | NEEDS_REVIEW | www.perfumersworld.com |
| botanical_name | elettaria cardamomum |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| botanical_name | elettaria cardamomum |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| botanical_name | elettaria cardamomum |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | www.scentspiracy.com |
| botanical_name | elettaria cardamomum |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | elettaria cardamomum |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | elettaria cardamomum |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | elettaria cardamomum |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | Eliettaria cardamomum. |  | SECONDARY_REFERENCE SDS | EXACT_CAS_ONLY | NEEDS_REVIEW | www.lookchem.com |
| iso_standard | ISO 4733 |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| iso_standard | ISO 4733:2004 |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| clp_class | Flam. Liq. 3 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| clp_class | Asp. Tox. 1 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| clp_class | Skin Irrit. 2 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| clp_class | Skin Sens. 1 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| clp_class | Eye Irrit. 2A |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| clp_class | Aquatic Chronic 2 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| clp_class | Aquatic Acute 2 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | ultrainternational.com |
| h_statement | H226 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H315 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H319 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H317 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H304 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H411 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H227 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
| h_statement | H303 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
| h_statement | H315 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
| h_statement | H317 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
| h_statement | H319 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
| h_statement | H411 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | EXACT_CAS_ONLY | NEEDS_REVIEW | finefrag.com |
_… 62 claims más en data/staging.sqlite_

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** vapour_pressure=0.13 hPa (MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF), NEEDS_REVIEW)
**SDS/CLP (por SDS, sin mezclar):** finefrag.com: H227, H303, H315, H317, H319, H411, Warning · ultrainternational.com: Aquatic Acute 2, Aquatic Chronic 2, Asp. Tox. 1, Danger, Eye Irrit. 2A, Flam. Liq. 3, H226, H304, H315, H317, H319, H401, H411, Skin Irrit. 2, Skin Sens. 1 · www.nhrorganicoils.com: Danger, H226, H304, H315, H317, H319, H411

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only] — valores: 57 C [SECONDARY]; 65 °C [SECONDARY]; 65 C [SECONDARY]; 59°C [SECONDARY]; 59 C [SECONDARY]
- `cas`: source CAS not in master CAS set — valores: 85940-32-5 [SECONDARY]; 85940-32-5 [SECONDARY]; 93062-62-5 [SECONDARY]; 8000-66-6 [SECONDARY]; 8000-66-6 [SECONDARY]; 8000-66-6 [SECONDARY]; 8000-66-6 [SECONDARY]; 8000-66-6 [MASTER]
- `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] — valores: H226 [SECONDARY]; H315 [SECONDARY]; H319 [SECONDARY]; H317 [SECONDARY]; H304 [SECONDARY]; H411 [SECONDARY]; H227 [SECONDARY]; H303 [SECONDARY]

**Cambios propuestos:** 14 (NEEDS_REVIEW: 14)

- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H226, H304, H315, H317, H319, H411
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H227, H303, H315, H317, H319, H411
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes=Aquatic Acute 2; Aquatic Chronic 2; Asp. Tox. 1; Eye Irrit. 2A; Flam. Liq. 3; Skin Irrit. 2; Skin Sens. 1 | H: H226, H304, H…
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=sabinene, Sample relative peak area %=4.3
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=limonene, Sample relative peak area %=2.1
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=1,8-cineole, Sample relative peak area %=29.2
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalool, Sample relative peak area %=3.6
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalyl acetate, Sample relative peak area %=5.7
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=alpha-terpinyl acetate, Sample relative peak area %=43.4
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=geraniol, Sample relative peak area %=0.7
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalyl acetate, Sample relative peak area %=6.95
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=limonene, Sample relative peak area %=4.39
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalool, Sample relative peak area %=4.17
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/lmr-compendium/): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Resolver conflicto en `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only]
- Resolver conflicto en `cas`: source CAS not in master CAS set
- Resolver conflicto en `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only]
- La composición GC-MS publicada es REFERENCE_COMPOSITION (muestras de investigación), nunca la botella ISIPCA; falta CoA/especificación del lote.

---

## N-0556 — BERGAMOT OIL DEFUROCOUMARI NIZED

*Grupo piloto:* NATURAL · *Qué prueba:* natural GC-MS, ISO 3520, FCF processing, SDS
*Estado final:* **NEEDS_REVIEW** — 1 conflicts; 12 changes need review
*Master antes:* tier `C_GENERIC_NATURAL_REFERENCE`, CAS `68648-33-9`, readiness 55 (PARTIAL)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 55 (PARTIAL); si se aprueban también los NEEDS_REVIEW → 57 (PARTIAL)

**Queries realizadas**

- `claude_websearch` · bergamot oil furocoumarin free LMR IFF → 9 resultados
- `claude_websearch` · Citrus bergamia peel essential oil GC-MS composition limonene linalyl acetate bergapten → 9 resultados
- `claude_websearch` · ISO 3520 bergamot oil Italian type → 10 resultados
- `claude_websearch` · bergamot oil FCF furocoumarin-free safety data sheet CAS 68648-33-9 → 9 resultados
- `claude_websearch` · bergamot oil Calabria origin furocoumarin removal bergapten FCF process → 9 resultados
- `claude_websearch` · bergamot oil use level perfumery IFRA bergapten limit → 9 resultados
- `claude_websearch` · "bergamot oil defurocoumarinized" → 9 resultados
- `claude_websearch` · bergamot oil Italy FCF LMR Naturals compendium → 9 resultados
- `ncbi_pmc_api` · (bergamot[Title] OR "Citrus bergamia"[Title]) AND (GC-MS OR "gas chromatography" OR composition) AND oil → 12 resultados

**Fuentes encontradas:** 63 URLs distintas; 13 seleccionadas para descarga (FETCHED: 6, MANUAL_RETRIEVAL_REQUIRED: 4, ROBOTS_DISALLOWED: 2, ENV_UNREACHABLE: 1); 15 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://www.iff.com/scent/lmr-compendium/bergamot-oil-cp-italy-org-fcr-csm/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://doi.org/10.3390/foods12010203 — MANUAL_RETRIEVAL_REQUIRED (HTTP 403 (site refuses automated access; not bypassed))
- https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/bergamot-essential-oil — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.tandfonline.com/doi/full/10.3109/13880200903486636 — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.avenalab.com/images/001SDS/MSDS2023/BERGAMOT-ESSENTIAL-OIL-FCF-BERGAPTEN-FREE-MSDS.pdf — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: ('Connection aborted.', Connec…)
- https://www.sciencedirect.com/science/article/pii/S0039914025000657 — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.iff.com/scent/lmr-compendium/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Exploring the Mechanism of Bergamot Essential Oil against A…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=10034984&rettype=xml) | peer-reviewed article; species found: citrus bergamia; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Aromatherapy: composition of the gaseous phase at equilibri…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=5668225&rettype=xml) | peer-reviewed article; species found: citrus bergamia; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Enhanced insecticidal efficacy of nanoencapsulated bergamot…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=13379571&rettype=xml) | peer-reviewed article; species found: citrus bergamia; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Translational Value of the Transdermal Administration of Be…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=9143031&rettype=xml) | peer-reviewed article; species found: citrus bergamia; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Determination of the Antifungal, Antibacterial Activity and…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=9818623&rettype=xml) | peer-reviewed article; species found: citrus bergamia; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Determination of the Antifungal, Antibacterial Activity and…](https://pubmed.ncbi.nlm.nih.gov/36613419/) | trade/common name in title: 'citrus bergamia'; species match citrus bergamia; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Bergamottin and 5-Geranyloxy-7-methoxycoumarin Cooperate in…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=8069240&rettype=xml) | peer-reviewed article; species found: citrus bergamia; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Bergamot Essential Oil Attenuates Anxiety-Like Behaviour in…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=6154596&rettype=xml) | peer-reviewed article; species found: citrus bergamia; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Mechanisms Underlying the Anti-Inflammatory Activity of Ber…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=7356015&rettype=xml) | peer-reviewed article; species found: citrus bergamia; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [High Quality Bergamot Oil from Greece: Chemical Analysis Us…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=6253838&rettype=xml) | peer-reviewed article; species found: citrus bergamia; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Material Safety Data Sheet: Bergamot Oil FCF Organic. Page …](https://www.nhrorganicoils.com/uploads/20160817124803e_Bergamot_Bergapten_Free_SDS.pdf) | trade/common name in title: 'bergamot oil'; title names another grade ('fcf'); species match citrus bergamia; reference for the natural type (not the school bo… |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Bergamot “Superior” Oil, FCF – Fraterworks](https://fraterworks.com/products/bergamot-oil-fcf) | trade/common name in text: 'citrus bergamia'; CAS match ['68648-33-9']; species match citrus bergamia; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Bergamot Oil FCF, Organic – Fraterworks](https://fraterworks.com/products/bergamot-oil-fcf-organic) | trade/common name in title: 'bergamot oil'; CAS match ['68648-33-9']; title names another grade ('fcf'); species match citrus bergamia; reference for the natur… |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Bergamot Oil FCF, Terpeneless – Fraterworks](https://fraterworks.com/products/bergamot-oil-terpeneless) | trade/common name in title: 'bergamot oil'; labelled CAS ['89957-91-5'] not in master set ['68648-33-9']; title names another grade ('fcf'); species match citr… |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [In vitro activity of bergamot natural essence and furocoumarin-free a…](https://pubmed.ncbi.nlm.nih.gov/15574476/) — trade/common name in text: 'bergamot oil'; common name only in body text

**Confianza de identidad:** LIKELY_MATCH (score 0.70)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 68648-33-9 |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| cas | 68648-33-9 |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| cas | 89957-91-5 |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | CONFLICT | fraterworks.com |
| tenacity | Lasts 4 hours on a smelling strip. | 4.0 hours | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| tenacity | Lasts 4 hours on a smelling strip. | 4.0 hours | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| density | 0.863-0.873 | 0.868 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| refractive_index | 1.458-1.468 | 1.463 nD | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| physical_state | Pale yellow liquid |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| physical_state | Pale yellow liquid |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| physical_state | Colourless liquid |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| botanical_name | citrus bergamia |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | citrus bergamia |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | citrus bergamia |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | citrus bergamia |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | citrus bergamia |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | citrus bergamia |  | PUBLISHED | LIKELY_MATCH | VALID | pubmed.ncbi.nlm.nih.gov |
| botanical_name | citrus bergamia |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | citrus bergamia |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | citrus bergamia |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | citrus bergamia |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | citrus bergamia |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| botanical_name | CITRUS AURANTIUM BERGAMIA FRUIT OIL |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| botanical_name | citrus bergamia |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| botanical_name | CITRUS AURANTIUM BERGAMIA FRUIT OIL |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| botanical_name | citrus bergamia |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| botanical_name | citrus bergamia |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| origin | Calabria, Italy |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| h_statement | H226 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H304 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H315 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H317 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H411 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H302 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H314 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| h_statement | H410 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| signal_word | Danger |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| sds_product_name | Product Name Bergamot Oil FCF Organic. |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| sds_component_cas | 5989-27-5 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| sds_component_cas | 115-95-7 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| sds_component_cas | 78-70-6 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| sds_component_cas | 127-91-3 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| sds_component_cas | 99-85-4 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| sds_component_cas | 123-35-3 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| sds_component_cas | 80-56-8 |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| stability_text | stable if used according to storage & handling conditions & identifie… |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.nhrorganicoils.com |
| gcms_study | Exploring the Mechanism of Bergamot Essential Oil against Asthma Base… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Aromatherapy: composition of the gaseous phase at equilibrium with li… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Enhanced insecticidal efficacy of nanoencapsulated bergamot essential… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Translational Value of the Transdermal Administration of Bergamot Ess… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Determination of the Antifungal, Antibacterial Activity and Volatile … |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Bergamottin and 5-Geranyloxy-7-methoxycoumarin Cooperate in the Cytot… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Bergamot Essential Oil Attenuates Anxiety-Like Behaviour in Rats |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | Mechanisms Underlying the Anti-Inflammatory Activity of Bergamot Esse… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| gcms_study | High Quality Bergamot Oil from Greece: Chemical Analysis Using Chiral… |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| composition:beta-pinene | 0.05-5.15 | 0.05–5.15 % (relative peak area unless stated) | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| composition:gamma-terpinene | 0.88-10.32 | 0.88–10.32 % (relative peak area unless stated) | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| composition:limonene | 0.65-34.88 | 0.65–34.88 % (relative peak area unless stated) | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| composition:linalool | 9.4 | 9.4 % (relative peak area unless stated) | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| composition:linalool | 46.34% | 46.34 % (relative peak area unless stated) | PUBLISHED | LIKELY_MATCH | VALID | pubmed.ncbi.nlm.nih.gov |
| composition:linalool | 1.75-34.62 | 1.75–34.62 % (relative peak area unless stated) | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
_… 3 claims más en data/staging.sqlite_

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** tenacity=Lasts 4 hours on a smelling s… (RETAILER (SECONDARY CLAIM), VALID); tenacity=Lasts 4 hours on a smelling s… (RETAILER (SECONDARY CLAIM), VALID)
**SDS/CLP (por SDS, sin mezclar):** www.nhrorganicoils.com: Danger, H226, H302, H304, H314, H315, H317, H410, H411

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `cas`: source CAS not in master CAS set — valores: 89957-91-5 [RETAILER]; 68648-33-9 [RETAILER]; 68648-33-9 [RETAILER]; 68648-33-9 [MASTER]

**Cambios propuestos:** 13 (NEEDS_REVIEW: 13)

- `NEEDS_REVIEW` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=4.0, unit=hours
- `NEEDS_REVIEW` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=4.0, unit=hours
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H226, H302, H304, H314, H315, H317, H410, H411
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalool, Sample relative peak area %=9.4
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalyl acetate, Sample relative peak area %=1.21
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalyl acetate, Sample relative peak area %=17.69%
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalool, Sample relative peak area %=46.34%
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=beta-pinene, Sample relative peak area %=0.05-5.15
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=limonene, Sample relative peak area %=0.65-34.88
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=gamma-terpinene, Sample relative peak area %=0.88-10.32
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalool, Sample relative peak area %=1.75-34.62
- `NEEDS_REVIEW` · NATURAL GCMS STUDIES · APPEND_ROW · Analyte=linalyl acetate, Sample relative peak area %=10.72-40.51
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/lmr-compendium/bergamot-oil-cp-italy-org-fcr-csm/): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Resolver conflicto en `cas`: source CAS not in master CAS set
- 1 documento(s) de identidad ambigua esperan revisión humana.
- La composición GC-MS publicada es REFERENCE_COMPOSITION (muestras de investigación), nunca la botella ISIPCA; falta CoA/especificación del lote.

---

## N-0728 — TUBEROSE ABS INDIA LMR

*Grupo piloto:* DIFFICULT · *Qué prueba:* suspected master error: botanical Rosa x damascena + rose CAS on a tuberose absolute -> botanical CONFLICT
*Estado final:* **NEEDS_REVIEW** — 3 conflicts; 4 changes need review
*Master antes:* tier `C_CLOSE_OR_AMBIGUOUS_REFERENCE`, CAS `8007-01-0`, readiness 18 (NOT_READY)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 18 (NOT_READY); si se aprueban también los NEEDS_REVIEW → 20 (NOT_READY)

**Queries realizadas**

- `claude_websearch` · tuberose absolute India LMR Naturals IFF → 9 resultados
- `claude_websearch` · Polianthes tuberosa absolute GC-MS composition → 10 resultados
- `claude_websearch` · tuberose absolute CAS number 8024-05-3 → 10 resultados
- `claude_websearch` · tuberose absolute safety data sheet → 10 resultados
- `claude_websearch` · tuberose absolute India origin methyl anthranilate chemotype → 9 resultados
- `claude_websearch` · tuberose absolute use level perfumery → 9 resultados
- `claude_websearch` · tuberose absolute ISO standard → 9 resultados
- `claude_websearch` · "Tuberose Abs India" LMR → 10 resultados
- `ncbi_pmc_api` · ("Polianthes tuberosa"[Title] OR tuberose[Title]) AND (GC-MS OR "gas chromatography" OR volatile) → 5 resultados

**Fuentes encontradas:** 59 URLs distintas; 23 seleccionadas para descarga (FETCHED: 12, MANUAL_RETRIEVAL_REQUIRED: 7, ROBOTS_DISALLOWED: 4); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://iff.com/en/scent/lmr-naturals/online-compendium — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/lmr-compendium/tuberose-abs-india-traceable/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://doi.org/10.3390/pr7020060 — MANUAL_RETRIEVAL_REQUIRED (HTTP 403 (site refuses automated access; not bypassed))
- https://www.researchgate.net/publication/293462159_Phytochemical_investigation_of_Polianthes_tuberosa — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.chemicalbook.com/ChemicalProductProperty_EN_CB91075246.htm — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 429 (site refuses automated access; not bypassed))
- https://www.chemicalbook.com/ChemicalProductProperty_US_CB91075246.aspx — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 429 (site refuses automated access; not bypassed))
- https://www.thegoodscentscompany.com/data/ab1005391.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/ab1005391.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://www.thegoodscentscompany.com/data/ab1101401.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/ab1101401.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://manuals.plus/m/094a6be0fb8b5f3ed09a99ab50d1b8a1464449079dff87bf81f5011295fe9489 — MANUAL_RETRIEVAL_REQUIRED (HTTP 403 (site refuses automated access; not bypassed))
- https://www.thegoodscentscompany.com/data/ab1055461.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/ab1055461.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://www.fragrantica.com/notes/Tuberose-25.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /notes/Tuberose-25.html -> MANUAL_RETRIEVAL_REQUIRED)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| LIKELY_MATCH | OFFICIAL_MANUFACTURER | UNKNOWN_LICENSE | [Tuberose absolute - Robertet Groupe – Tuberose absolute ing…](https://matieres-premieres.robertet.com/tuberose-absolute) | trade/common name in title: 'tuberose absolute'; official manufacturer domain (Robertet); species match polianthes tuberosa; reference for the natural type (no… |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Page: 1 / 8](https://shop.perfumersapprentice.com/msds/9309.pdf) | trade/common name in text: 'polianthes tuberosa'; species match polianthes tuberosa; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [Metabolic and molecular basis of floral scent differentiati…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=13358669&rettype=xml) | peer-reviewed article; species found: agave amica; REFERENCE_COMPOSITION only (research sample, not the school bottle) |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [TUBEROSE ABSOLUTE](https://www.ventos.com/index.php/en/producto/1509/TUBEROSE+ABSOLUTE/223) | trade/common name in title: 'tuberose absolute'; species match polianthes tuberosa; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Tuberose Absolute /](https://www.perfumersworld.com/view.php?pro_id=8ND00451) | trade/common name in title: 'tuberose absolute'; species match polianthes tuberosa; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | PEER_REVIEWED | PRODUCTION_SAFE_WITH_CITATION | [STUDY OF THE BIOACTIVE COMPOUNDS CONTENT IN THE FLOWERS OF …](https://pubmed.ncbi.nlm.nih.gov/34749339/) | trade/common name in title: 'polianthes tuberosa'; species match polianthes tuberosa; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Tuberose Absolute - Polianthes Tuberosa- India - PB-1111TK …](https://bulkaroma.com/products/tuberose-absolute-polianthes-tuberosa-absolute-pe-1202up) | trade/common name in title: 'polianthes tuberosa'; species match polianthes tuberosa; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [TECHNICAL DATA SHEET](https://www.greenleafextractions.com/storage/3289/TUBEROSE---ABSOLUTE---TDS.pdf) | trade/common name in text: 'polianthes tuberosa'; labelled CAS ['8024-05-3'] not in master set ['8007-01-0']; species match polianthes tuberosa; reference for … |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Tuberose “Signature” Absolute – Fraterworks](https://fraterworks.com/products/tuberose-signature-absolute) | trade/common name in text: 'polianthes tuberosa'; labelled CAS ['94334-35-7'] not in master set ['8007-01-0']; expected manufacturer 'LMR Naturals (IFF)' menti… |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Tuberose Absolute for Natural Perfumery from hermitageoils.…](https://hermitageoils.com/product/tuberose-absolute/) | trade/common name in title: 'tuberose absolute'; species match polianthes tuberosa; reference for the natural type (not the school bottle) |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Tuberose Absolute - Fine / Eden Botanicals](https://www.edenbotanicals.com/tuberose-absolute-fine.html) | trade/common name in title: 'tuberose absolute'; labelled CAS ['8024-05-3'] not in master set ['8007-01-0']; species match polianthes tuberosa; reference for t… |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Tuberoseabsolute SDS, 8024-05-3 Safety Data Sheets - ECHEMI](https://www.echemi.com/sds/tuberoseabsolute-pid_Rock27439.html) | trade/common name in text: 'polianthes tuberosa'; species match polianthes tuberosa; reference for the natural type (not the school bottle) |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [Exploring the Chemical Composition of Bulgarian Lavender Absolute (La…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=9692913&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)
- [SAFETY DATA SHEET](http://ultrainternational.com/wp-content/uploads/2023/08/SDS-TUBEROSE-ABSOLUTE.pdf) — trade/common name in text: 'tuberose absolute'; labelled CAS ['8024-05-3', '94334-35-7'] not in master set ['8007-01-0']; common name only in body text

**Confianza de identidad:** LIKELY_MATCH (score 0.70)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 8024-05-3 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| cas | 94334-35-7 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| cas | 8024-05-3 |  | SECONDARY_REFERENCE | LIKELY_MATCH | CONFLICT | www.greenleafextractions.com |
| cas | 94334-35-7 |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | CONFLICT | fraterworks.com |
| cas | 8024-05-3 |  | SECONDARY_REFERENCE | LIKELY_MATCH | CONFLICT | www.edenbotanicals.com |
| tenacity | Lasts > 200 hours on a smelling strip. | 200.0 hours | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| density | 0,9520 | 0.952 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| density | 0.940 - 0.990 @25°C | 0.965 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| density | 0.940-0.990 | 0.965 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| density | 0.915-0.990 | 0.9525 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | bulkaroma.com |
| density | 0.9660 | 0.966 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | bulkaroma.com |
| refractive_index | 1.485 - 1.500 @20°C | 1.4925 nD | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| refractive_index | 1.485-1.500 | 1.4925 nD | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| refractive_index | 1.475-1.510 | 1.4925 nD | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | bulkaroma.com |
| refractive_index | 1.492 | 1.492 nD | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | bulkaroma.com |
| flash_point | > 100,0 °C NFT 60-103 CC | 100.0 C | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| flash_point | >100,0 C | 100.0 C | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| flash_point | >93°C | 93.0 C | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| flash_point | >93 C | 93.0 C | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| physical_state | liquid to semi-crystallized |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| physical_state | Liquid |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| physical_state | Deep orange liquid |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| physical_state | Dark reddish-orange. This product ranges from very viscous liquid to … |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| product_code | UL3000168 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| product_code | FL-346802 |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.greenleafextractions.com |
| ec_number | 202-590-7 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| ec_number | 202-589-1 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| ec_number | 202-859-9 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| ec_number | 201-134-4 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| ec_number | 207-431-5 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| ec_number | European Inventory of Existing Commercial Chemical Substances |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| ec_number | European List of Notified Chemical Substances |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| ec_number | 305-108-4 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| botanical_name | polianthes tuberosa |  | MANUFACTURER | LIKELY_MATCH | VALID | matieres-premieres.robertet.com |
| botanical_name | polianthes tuberosa |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| botanical_name | agave amica |  | PUBLISHED | LIKELY_MATCH | VALID | eutils.ncbi.nlm.nih.gov |
| botanical_name | polianthes tuberosa |  | DISTRIBUTOR_SPEC | LIKELY_MATCH | NEEDS_REVIEW | www.ventos.com |
| botanical_name | polianthes tuberosa |  | DISTRIBUTOR_SPEC | LIKELY_MATCH | NEEDS_REVIEW | www.perfumersworld.com |
| botanical_name | rosa damascena |  | DISTRIBUTOR_SPEC | LIKELY_MATCH | NEEDS_REVIEW | www.perfumersworld.com |
| botanical_name | polianthes tuberosa |  | PUBLISHED | LIKELY_MATCH | VALID | pubmed.ncbi.nlm.nih.gov |
| botanical_name | polianthes tuberosa |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | bulkaroma.com |
| botanical_name | polianthes tuberosa |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.greenleafextractions.com |
| botanical_name | polianthes tuberosa |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| botanical_name | Polianthes tuberosa |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | hermitageoils.com |
| botanical_name | polianthes tuberosa |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | hermitageoils.com |
| botanical_name | Polianthes tuberosa L. |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| botanical_name | Polianthes Tuberosa (Tuberose) Flower Extract |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| botanical_name | polianthes tuberosa |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| botanical_name | polianthes tuberosa |  | SECONDARY_REFERENCE SDS | LIKELY_MATCH | NEEDS_REVIEW | www.echemi.com |
| extraction_method | Solvent Extracted |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | www.edenbotanicals.com |
| origin | France |  | SECONDARY_REFERENCE | LIKELY_MATCH | NEEDS_REVIEW | hermitageoils.com |
| iso_standard | ISO 3515:2002 |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| clp_class | Aquatic Acute 3 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| clp_class | Aquatic Chronic 3 |  | RETAILER (SECONDARY CLAIM) SDS | LIKELY_MATCH | VALID | shop.perfumersapprentice.com |
| clp_class | Skin Irrit. 2 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| clp_class | Skin Sens. 1 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| clp_class | Muta. 2 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| clp_class | Carc. 2 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| clp_class | Repr. 2 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
| clp_class | Asp. Tox. 1 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | ultrainternational.com |
_… 47 claims más en data/staging.sqlite_

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** tenacity=Lasts > 200 hours on a smelli… (RETAILER (SECONDARY CLAIM), VALID)
**SDS/CLP (por SDS, sin mezclar):** shop.perfumersapprentice.com: Aquatic Acute 3, Aquatic Chronic 3, H317, H332, H402, H412, Warning · www.echemi.com: H302, H317, H332, H412

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `cas`: source CAS not in master CAS set — valores: 8024-05-3 [SECONDARY]; 94334-35-7 [RETAILER]; 8024-05-3 [SECONDARY]; 8007-01-0 [MASTER]
- `botanical_species`: sources identify polianthes tuberosa; master says 'Rosa x damascena (typical source; not stated for all grades)' — valores: polianthes tuberosa [OFFICIAL_MANUFACTURER]; polianthes tuberosa [RETAILER]; agave amica [PEER_REVIEWED]; polianthes tuberosa [DISTRIBUTOR]; polianthes tuberosa [DISTRIBUTOR]; polianthes tuberosa [PEER_REVIEWED]; polianthes tuberosa [RETAILER]; polianthes tuberosa [SECONDARY]
- `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only] — valores: H332 [RETAILER]; H317 [RETAILER]; H402 [RETAILER]; H412 [RETAILER]; H302 [SECONDARY]; H317 [SECONDARY]; H332 [SECONDARY]; H412 [SECONDARY]

**Cambios propuestos:** 5 (NEEDS_REVIEW: 4, BLOCKED_CONFLICT: 1)

- `NEEDS_REVIEW` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=>200.0, unit=hours
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes=Aquatic Acute 3; Aquatic Chronic 3 | H: H317, H332, H402, H412
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H302, H317, H332, H412
- `BLOCKED_CONFLICT` · NATURAL IDENTITY · UPDATE_CELL · botanical_species: Rosa x damascena (typical source; not stated for all grades) → polianthes tuberosa
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://iff.com/en/scent/lmr-naturals/online-compendium): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Resolver conflicto en `cas`: source CAS not in master CAS set
- Resolver conflicto en `botanical_species`: sources identify polianthes tuberosa; master says 'Rosa x damascena (typical source; not stated for all grades)'
- Resolver conflicto en `h_statement`: SDS from different suppliers/grades list different H statements (reported per SDS; not merged) [lower-tier dissent only]
- 2 documento(s) de identidad ambigua esperan revisión humana.
- La composición GC-MS publicada es REFERENCE_COMPOSITION (muestras de investigación), nunca la botella ISIPCA; falta CoA/especificación del lote.

---

## S-0507 — AMBER XTREME TM

*Grupo piloto:* DIFFICULT · *Qué prueba:* no CAS, trademark name, ambiguous identity
*Estado final:* **NEEDS_REVIEW** — 0 conflicts; 4 changes need review
*Master antes:* tier `D_FAMILY_LEVEL_ONLY`, CAS `None`, readiness 0 (NOT_READY)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 0 (NOT_READY); si se aprueban también los NEEDS_REVIEW → 20 (NOT_READY)

**Queries realizadas**

- `claude_websearch` · Amber Xtreme IFF → 10 resultados
- `claude_websearch` · "Amber Xtreme" CAS → 9 resultados
- `claude_websearch` · Amber Xtreme safety data sheet → 9 resultados
- `claude_websearch` · Amber Xtreme perfumery ingredient → 9 resultados
- `claude_websearch` · Amber Xtreme use level → 9 resultados
- `claude_websearch` · Amber Xtreme captive ambergris molecule composition → 9 resultados
- `claude_websearch` · "Amber Xtreme" odor → 9 resultados
- `pubchem_api` · name:amber xtreme → 0 resultados

**Fuentes encontradas:** 38 URLs distintas; 18 seleccionadas para descarga (FETCHED: 13, ROBOTS_DISALLOWED: 2, MANUAL_RETRIEVAL_REQUIRED: 1, ENV_UNREACHABLE: 2); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://cosmetics.specialchem.com/product/i-iff-amber-xtreme — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.iff.com/scent/ingredients-compendium/amber-xtreme-2/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://ir.iff.com/news-releases/news-release-details/iff-launches-amber-xtremetm — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: HTTPSConnectionPool(host='ir.i…)
- http://lmrnaturals.iff.com/en/site-services/online-compendium-new/amber-xtreme — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: ('Connection aborted.', Connec…)
- https://www.fragrantica.com/notes/Amber-Xtreme-879.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /notes/Amber-Xtreme-879.html -> MANUAL_RETRIEVAL_REQUI…)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [AMBER XTREME™ IFF](https://www.ventos.com/index.php/en/producto/7833/AMBER+XTREME+IFF/AMBER+XTREME%E2%84%A2+IFF) | trade/common name in title: 'amber xtreme' |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Amber Xtreme™ (476332-65-7) – Premium Synthetic Ingredient …](https://www.scentspiracy.com/fragrance-ingredients/p/amberxtreme) | trade/common name in title: 'amber xtreme'; SDS issued by IFF (section 1), hosted by a third party |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Perfumers Apprentice - Amber Xtreme™ (IFF) **](https://shop.perfumersapprentice.com/p-8055-amber-xtreme-iff.aspx) | trade/common name in title: 'amber xtreme' |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Amber Xtreme - IFF – Bulkaroma](https://bulkaroma.com/products/amber-xtreme-iff) | trade/common name in title: 'amber xtreme' |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Amber Xtreme - IFF – Global Perfumes Shop](https://globalperfumesshop.com/products/amber-xtreme-iff) | trade/common name in title: 'amber xtreme' |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [Amber xtreme (IFF) Online Kopen bij Hekserij](https://eng.hekserij.nl/shop/fragrance-raw-material/search-by-type/aroma-chemicals/amber-xtreme-iff/) — trade/common name in title: 'amber xtreme'; title describes a different product ('type'); title names another grade ('type')
- [Ambrafuran (AmbroxTM) Synthesis from Natural Plant Product Precursors](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=7504449&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)
- [SAFETY DATA SHEET](https://shop.perfumersapprentice.com/Images/sds/AMBER%20XTREME%20TM%20GHS%20SDS.pdf) — trade/common name in text: 'amber xtreme'; name only in body text
- [SAFETY DATA SHEET](https://johndwalsh.com/wp-content/uploads/2026/07/AMBER-XTREME-TM.pdf) — trade/common name in text: 'amber xtreme'; name only in body text
- [Fragrance Product Information Sheet (FPIS)](https://perfumersupplyhouse.com/wp-content/uploads/2015/09/AMBER-XTREME-TM-FPIS.pdf) — trade/common name in text: 'amber xtreme'; name only in body text
- [Product Data Sheet](https://finefrag.com/wp-content/uploads/2019/11/AMBER-XTREME-TM.pdf) — trade/common name in text: 'amber xtreme'; name only in body text

**Fuentes rechazadas:** 3

- Ultramber® Xtreme – Fraterworks — page is about another trade product ('Ultramber'); neither trade name nor CAS found
- AMBER — neither trade name nor CAS found
- Amber Products Safety Data Sheet — neither trade name nor CAS found

**Confianza de identidad:** LIKELY_MATCH (score 0.65)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 476332-65-7 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| cas | 476332-65-7 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| cas | 476332-65-7 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| cas | 476332-65-7 |  | SECONDARY_REFERENCE | AMBIGUOUS | NEEDS_REVIEW | perfumersupplyhouse.com |
| use_level | up to 0,5% | None–0.5 % | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| vapour_pressure | < 0.01 hPa | 1.0 Pa | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| vapour_pressure | 0.01 hPa | 1.0 Pa | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| vapour_pressure | < 0.01 hPa (68 °F / 20 °C) | 1.0 Pa | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| vapour_pressure | 0.01 hPa | 1.0 Pa | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| vapour_pressure | 0,7 Pa | 0.7 Pa | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| logp | 0,71 | 0.71 log10 | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| density | 0.9380 - 0.9460 | 0.942 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| density | 0.9380-0.9460 | 0.942 g/cm3 (or SG, ~equal at 20-25 C) | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| density | 0,94 | 0.94 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| flash_point | 128 °C | 128.0 C | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| flash_point | 128 C | 128.0 C | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| flash_point | 262 °F / 128 °C | 127.8 C | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| flash_point | 262 F | 127.8 C | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| flash_point | 128 C | 128.0 C | SECONDARY_REFERENCE | AMBIGUOUS | NEEDS_REVIEW | finefrag.com |
| physical_state | liquid |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| physical_state | liquid |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| ec_number | 449-360-4 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | eng.hekserij.nl |
| iso_standard | ISO 9235 |  | SECONDARY_REFERENCE | AMBIGUOUS | NEEDS_REVIEW | perfumersupplyhouse.com |
| iso_standard | ISO 16128 |  | SECONDARY_REFERENCE | AMBIGUOUS | NEEDS_REVIEW | perfumersupplyhouse.com |
| h_statement | H316 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| h_statement | H317 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| h_statement | H410 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| h_statement | H317 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| h_statement | H317 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | LIKELY_MATCH | VALID | www.scentspiracy.com |
| h_statement | H411 |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | LIKELY_MATCH | VALID | www.scentspiracy.com |
| signal_word | Warning |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| signal_word | Warning |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| signal_word | Warning |  | MANUFACTURER_SDS_VIA_THIRD_PARTY (IFF) | LIKELY_MATCH | VALID | www.scentspiracy.com |
| sds_product_name | AMBER XTREME TM |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| sds_product_name | AMBER XTREME TM |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| sds_component_cas | 476332-65-7 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| sds_component_cas | 476332-65-7 |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| stability_text | Stable under normal conditions. |  | SECONDARY_REFERENCE SDS | AMBIGUOUS | NEEDS_REVIEW | johndwalsh.com |
| gcms_study | Ambrafuran (AmbroxTM) Synthesis from Natural Plant Product Precursors |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| molecular_weight | 264 g/mol | 264.0 g/mol | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| additive_cas | 120-51-4 |  | SECONDARY_REFERENCE | AMBIGUOUS | NEEDS_REVIEW | perfumersupplyhouse.com |

**Evidencia de dosis:** up to 0,5% (RETAILER (SECONDARY CLAIM), eng.hekserij.nl, NEEDS_REVIEW)
**Evidencia de performance:** vapour_pressure=< 0.01 hPa (RETAILER (SECONDARY CLAIM) SDS, NEEDS_REVIEW); vapour_pressure=0.01 hPa (RETAILER (SECONDARY CLAIM) SDS, NEEDS_REVIEW); vapour_pressure=< 0.01 hPa (68 °F / 20 °C) (SECONDARY_REFERENCE SDS, NEEDS_REVIEW); vapour_pressure=0.01 hPa (SECONDARY_REFERENCE SDS, NEEDS_REVIEW); vapour_pressure=0,7 Pa (RETAILER (SECONDARY CLAIM), NEEDS_REVIEW)
**SDS/CLP (por SDS, sin mezclar):** www.scentspiracy.com: H317, H411, Warning

**Cambios propuestos:** 5 (NEEDS_REVIEW: 5)

- `NEEDS_REVIEW` · DOSE EVIDENCE STRUCTURED · APPEND_ROW · dose_type=SECONDARY_REFERENCE_MAX_USE, value_text=up to 0,5%, unit=%
- `NEEDS_REVIEW` · MATERIAL IDENTITY · UPDATE_CELL · resolved_cas: None → 476332-65-7
- `NEEDS_REVIEW` · MATERIAL IDENTITY · UPDATE_CELL · identity_tier: D_FAMILY_LEVEL_ONLY → B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK
- `NEEDS_REVIEW` · CLP HAZARDS · APPEND_ROW · hazard_classes= | H: H317, H411
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/ingredients-compendium/amber-xtreme-2/): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- 6 documento(s) de identidad ambigua esperan revisión humana.

---

## S-0023 — RHUBAFURAN TOCO

*Grupo piloto:* DIFFICULT · *Qué prueba:* no CAS in master, identity improvement
*Estado final:* **NEEDS_REVIEW** — 0 conflicts; 6 changes need review
*Master antes:* tier `D_FAMILY_LEVEL_ONLY`, CAS `None`, readiness 20 (NOT_READY)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 20 (NOT_READY); si se aprueban también los NEEDS_REVIEW → 50 (PARTIAL)

**Queries realizadas**

- `claude_websearch` · Rhubafuran fragrance ingredient manufacturer → 9 resultados
- `claude_websearch` · Rhubafuran CAS → 10 resultados
- `claude_websearch` · Rhubafuran safety data sheet → 9 resultados
- `claude_websearch` · Rhubafuran use level → 10 resultados
- `claude_websearch` · Rhubafuran IFF → 10 resultados
- `claude_websearch` · Rhubafuran perfumery rhubarb odor → 9 resultados
- `claude_websearch` · Rhubafuran Givaudan → 10 resultados
- `pubchem_api` · name:rhubafuran → 0 resultados

**Fuentes encontradas:** 37 URLs distintas; 18 seleccionadas para descarga (FETCHED: 9, MANUAL_RETRIEVAL_REQUIRED: 6, ROBOTS_DISALLOWED: 3); 11 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://www.givaudan.com/fragrance-beauty/fragrance-ingredients-business/fragrance-molecules/rhubafuran — MANUAL_RETRIEVAL_REQUIRED (CAPTCHA page served (HTTP 200) - bot protection; not bypassed)
- https://www.scentree.co/en/Rhubafuran%C2%AE.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /en/Rhubafuran%C2%AE.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://www.thegoodscentscompany.com/data/rw1043021.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/rw1043021.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://www.chemicalbook.com/ChemicalProductProperty_EN_CB3197718.htm — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 429 (site refuses automated access; not bypassed))
- https://www.chemicalbook.com/msds/rhubafuran.pdf — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 429 (site refuses automated access; not bypassed))
- https://www.givaudan.com/fragrance-beauty/eindex/rhubafuran — MANUAL_RETRIEVAL_REQUIRED (CAPTCHA page served (HTTP 200) - bot protection; not bypassed)
- http://m.molbase.com/moldata/191303.html — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.ulprospector.com/en/na/PersonalCare/Detail/31183/994914/Rhubafuran — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.givaudan.com/files/8683003_formula.pdf — MANUAL_RETRIEVAL_REQUIRED (CAPTCHA page served (HTTP 200) - bot protection; not bypassed)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| LIKELY_MATCH | IDENTITY_DB | PRODUCTION_SAFE_WITH_ATTRIBUTION | [Rhubafuran / C12H16O / CID 113514 - PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/Rhubafuran) | trade/common name in title: 'rhubafuran' |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [SAFETY DATA SHEET](https://www.vigon.com/product/rhubafuran/?doc=MSDS%2F503248_vigon_sds_us_english.pdf&namee=RhubafuranSDS) | trade/common name in title: 'rhubafuran' |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [Rhubafuran - Vigon](https://www.vigon.com/product/rhubafuran/) | trade/common name in title: 'rhubafuran' |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Perfumers Apprentice - Rhubafuran (Givaudan)](https://shop.perfumersapprentice.com/p-6214-rhubafuran-givaudan.aspx) | trade/common name in title: 'rhubafuran' |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Rhubafuran - GIVAUDAN – Bulkaroma](https://bulkaroma.com/products/rhubafuran-givaudan) | trade/common name in title: 'rhubafuran' |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Rhubafuran Givaudan / Perfume Material - Olfactorian](https://olfactorian.com/materials/rhubafuran-givaudan) | trade/common name in title: 'rhubafuran' |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [Occupational Exposure to Carbofuran and the Incidence of Cancer in th…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=1253753&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)
- [Modification of the existing maximum residue level for cyprodinil in …](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=7009263&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)
- [SAFETY DATA SHEET](https://shop.perfumersapprentice.com/Images/RhubafuranSDS.pdf) — trade/common name in text: 'rhubafuran'; name only in body text
- [Rhuboflor – Fraterworks](https://fraterworks.com/products/rhuboflor) — trade/common name in text: 'rhubafuran'; name only in body text

**Fuentes rechazadas:** 1

- Rhubofix | — neither trade name nor CAS found

**Confianza de identidad:** LIKELY_MATCH (score 0.65)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 93939-86-7 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| vapour_pressure | 0.01 mm Hg 20 | 1.33322 Pa | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| vapour_pressure | 0.01 mm Hg 20 | 1.33322 Pa | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| tenacity | Lasts > 48 hours on a smelling strip. | 48.0 hours | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| density | 0.99 | 0.99 g/cm3 (or SG, ~equal at 20-25 C) | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| density | 0.99 | 0.99 g/cm3 (or SG, ~equal at 20-25 C) | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| flash_point | >200.0 F | 93.3 C | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| flash_point | >200.0 F | 93.3 C | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| flash_point | 200°F (94°C) | 93.3 C | DISTRIBUTOR_SPEC | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| physical_state | Colourless liquid |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | fraterworks.com |
| h_statement | H303 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| h_statement | H315 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| signal_word | Warning |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| signal_word | Warning |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| sds_component_cas | 82461-14-1 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| sds_component_cas | 99343-91-6 |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| sds_component_cas | 82461-14-1 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| storage | store near an open flame, heat or other sources of ignition. |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| storage | store near an open flame, heat or other sources of ignition. |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| stability_text | stable and non-reactive under normal conditions of use, storage and t… |  | DISTRIBUTOR_SDS | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |
| stability_text | stable and non-reactive under normal conditions of use, storage and t… |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| gcms_study | Occupational Exposure to Carbofuran and the Incidence of Cancer in th… |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| gcms_study | Modification of the existing maximum residue level for cyprodinil in … |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| molecular_weight | 176.2600 | 176.26 g/mol | DISTRIBUTOR_SPEC | LIKELY_MATCH | NEEDS_REVIEW | www.vigon.com |

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** vapour_pressure=0.01 mm Hg 20 (DISTRIBUTOR_SDS, NEEDS_REVIEW); vapour_pressure=0.01 mm Hg 20 (RETAILER (SECONDARY CLAIM) SDS, NEEDS_REVIEW); tenacity=Lasts > 48 hours on a smellin… (RETAILER (SECONDARY CLAIM), NEEDS_REVIEW)
**SDS/CLP (por SDS, sin mezclar):** www.vigon.com: Warning

**Cambios propuestos:** 7 (NEEDS_REVIEW: 7)

- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=vapor_pressure_supplier, value=1.33322, unit=Pa (converted from 0.01 mm hg (temperature not stated))
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=density_20C, value=0.99, unit=g/cm3 (or SG, ~equal at 20-25 C)
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=>93.3, unit=C
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=93.3, unit=C
- `NEEDS_REVIEW` · MATERIAL IDENTITY · UPDATE_CELL · resolved_cas: None → 82461-14-1
- `NEEDS_REVIEW` · MATERIAL IDENTITY · UPDATE_CELL · identity_tier: D_FAMILY_LEVEL_ONLY → B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Sin SDS del producto analizable: pedir SDS al proveedor/escuela.
- 4 documento(s) de identidad ambigua esperan revisión humana.

---

## S-0020 — ALD C-11 INTRELEVEN (TT) PRG

*Grupo piloto:* DIFFICULT · *Qué prueba:* no CAS, chart code PRG, ambiguous aldehyde mixture
*Estado final:* **NEEDS_REVIEW** — 2 conflicts; 7 changes need review
*Master antes:* tier `D_FAMILY_LEVEL_ONLY`, CAS `None`, readiness 0 (NOT_READY)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 0 (NOT_READY); si se aprueban también los NEEDS_REVIEW → 33 (NOT_READY)

**Queries realizadas**

- `claude_websearch` · Intreleven aldehyde IFF → 10 resultados
- `claude_websearch` · Intreleven aldehyde CAS → 10 resultados
- `claude_websearch` · Intreleven aldehyde safety data sheet → 10 resultados
- `claude_websearch` · Intreleven aldehyde use level perfumery → 10 resultados
- `claude_websearch` · aldehyde C-11 Intreleven undecenal composition isomers → 10 resultados
- `claude_websearch` · "Intreleven" aldehyde odor → 10 resultados
- `claude_websearch` · Aldehyde C-11 Intreleven special PRG → 10 resultados
- `pubchem_api` · name:c-11 intreleven aldehyde → 0 resultados
- `pubchem_api` · name:aldehyde c-11 intreleven → 0 resultados
- `pubchem_api` · name:intreleven aldehyde → 0 resultados
- `pubchem_api` · name:ald c-11 intreleven → 0 resultados
- `pubchem_api` · name:aldehyde intreleven → 0 resultados

**Fuentes encontradas:** 35 URLs distintas; 26 seleccionadas para descarga (FETCHED: 14, MANUAL_RETRIEVAL_REQUIRED: 3, ENV_UNREACHABLE: 3, ROBOTS_DISALLOWED: 6); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://www.iff.com/scent/ingredients-compendium/intreleven-aldehyde/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/ingredients-compendium/intreleven-aldehyde-special/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- http://lmrnaturals.iff.com/en/scent/fragrance-ingredients/online-compendium-new/intreleven-aldehyde — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: ('Connection aborted.', Connec…)
- https://www.specialchem.com/cosmetics/product/iff-intreleven-aldehyde — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.specialchem.com/cosmetics/product/iff-intreleven-aldehyde-special — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.thegoodscentscompany.com/data/rw1395171.html — ROBOTS_DISALLOWED (robots.txt disallows ClaudeBot for /data/rw1395171.html -> MANUAL_RETRIEVAL_REQUIRED)
- https://www.chemicalbook.com/ChemicalProductProperty_EN_CB49917268.htm — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 429 (site refuses automated access; not bypassed))
- https://www.myskinrecipes.com/shop/en/aldehyde-aroma-chemicals/2458-intreleven-aldehyde.html — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.perfumerflavorist.com/roundups/2024/june/news/22912596/symrise-symrise-ags-intreleven-aldehyde-special — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.specialchem.com/cosmetics/product/symrise-intreleven-aldehyde-spec — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.creatingperfume.com/aldc11intrelevenaldehydespecialbhaiff.aspx — ENV_UNREACHABLE (robots.txt unreachable: HTTPSConnectionPool(host='www.creatingperfume.com', port=443): Ma…)
- https://www.creatingperfume.com/intrelevenaldehydespecialiff.aspx — ENV_UNREACHABLE (domain unreachable earlier in run: robots.txt unreachable: HTTPSConnectionPool(host='www.…)

**Fuentes aceptadas**

| match | tipo | licencia | documento | motivos |
|---|---|---|---|---|
| LIKELY_MATCH | OFFICIAL_MANUFACTURER | UNKNOWN_LICENSE | [stneidergnI](https://www.symrise.com/fileadmin/symrise/Marketing/Scent_and_care/Aroma_molecules/Ingredient_finder/SYM_PC_Datenblaetter/SYM_PC-Intereleven_Aldehyde_Spec..pdf) | trade/common name in text: 'intreleven aldehyde'; official manufacturer domain (Symrise); official Symrise document, but the manufacturer of the school bottle … |
| LIKELY_MATCH | DISTRIBUTOR | UNKNOWN_LICENSE | [ALDEHYDE INTRELEVEN](https://www.ventos.com/index.php/en/producto/2271/ALDEHYDE+INTRELEVEN/223) | trade/common name in title: 'aldehyde intreleven' |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Perfumers Apprentice - Intreleven Aldehyde (IFF) **](https://shop.perfumersapprentice.com/p-6117-intreleven-aldehyde-iff.aspx) | trade/common name in title: 'intreleven aldehyde' |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Aldehyde C-11 Intreleven – Fraterworks](https://fraterworks.com/products/aldehyde-c-11-intreleven) | trade/common name in title: 'aldehyde c-11 intreleven' |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Intreleven Aldehyde - BC Fragrance](https://shop.bcfragrance.com/product/intreleven-aldehyde-for-pre-order/) | trade/common name in title: 'intreleven aldehyde' |
| LIKELY_MATCH | RETAILER | RESEARCH_ONLY | [Intreleven Aldehyde from IFF-Aromatic Chemicals – Bulkaroma](https://bulkaroma.com/products/intreleven-aldehyde-iff) | trade/common name in title: 'intreleven aldehyde' |
| LIKELY_MATCH | SECONDARY | UNKNOWN_LICENSE | [Intreleven Aldehyde Manufacturer & Supplier / 112-45-8 / Ch…](https://www.chemicalbull.com/products/intreleven-aldehyde) | trade/common name in title: 'intreleven aldehyde' |

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [SAFETY DATA SHEET](https://shop.perfumersapprentice.com/msds/6117.pdf) — trade/common name in text: 'intreleven aldehyde'; name only in body text
- [Undecenal Mixture (Aldehyde C-11 Mixed) | Perfume Material - Olfactor…](https://olfactorian.com/materials/undecenal-mixture-aldehyde-c11-mixed) — trade/common name in text: 'intreleven aldehyde'; name only in body text
- [Perfumers Apprentice - Aldehydic](https://shop.perfumersapprentice.com/c-68-aldehydic.aspx) — trade/common name in text: 'intreleven aldehyde'; name only in body text
- [Aldehyde C-11 Undecylenic | Perfume Material - Olfactorian](https://olfactorian.com/materials/aldehyde-c11-undecylenic) — trade/common name in text: 'aldehyde c-11 intreleven'; name only in body text

**Fuentes rechazadas:** 3

- Noves fitxes EN — neither trade name nor CAS found; NO_CONTENT: only site template after removing 371 shared lines (page likely…
- Aldehyde C-11 Undecylenic | — neither trade name nor CAS found
- DirectPCW | Perfume Ingredients Specialist — trade/common name in title: 'intreleven'; neither trade name nor CAS found

**Confianza de identidad:** LIKELY_MATCH (score 0.75)

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| cas | 1337-83-3 |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| use_level | 0.1-2% | 0.1–2.0 % | MANUFACTURER | LIKELY_MATCH | VALID | www.symrise.com |
| vapour_pressure | .04 hPa (0.04 hPa) | 4.0 Pa | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| vapour_pressure | 04 hPa | 400.0 Pa | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| logp | 4.12 | 4.12 log10 | MANUFACTURER | LIKELY_MATCH | VALID | www.symrise.com |
| logp | n-octanol/water : log Pow: 3.970 | 3.97 log10 | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| logp | 3.970 | 3.97 log10 | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| tenacity | Lasts > 400 hours on a smelling strip. | 400.0 hours | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | CONFLICT | fraterworks.com |
| tenacity | 380 Hours | 380.0 hours | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | CONFLICT | shop.bcfragrance.com |
| substantivity_application | Moderate |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | shop.bcfragrance.com |
| flash_point | 89 C | 89.0 C | MANUFACTURER | LIKELY_MATCH | VALID_DISPUTED | www.symrise.com |
| flash_point | 174.20 °F (79.00 °C) | 79.0 C | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| flash_point | 174.20 F | 79.0 C | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| flash_point | 60 C | 60.0 C | SECONDARY_REFERENCE | LIKELY_MATCH | CONFLICT | www.chemicalbull.com |
| physical_state | liquid |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| physical_state | CLEAR LIQUID |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| physical_state | Colourless liquid |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| physical_state | Colorless liquid |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | shop.bcfragrance.com |
| odour_description | Aldehydic |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | fraterworks.com |
| odour_description | Fresh amber aldehydic mossy citrus tuberose metallic waxy coumarin |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| h_statement | H227 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| h_statement | H317 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| signal_word | Warning |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| sds_product_name | INTRELEVEN ALDEHYDE |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| sds_component_cas | 1337-83-3 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| sds_component_cas | 25013-16-5 |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| stability_text | Remarks: Presents no significant reactivity hazard, by itself or in |  | RETAILER (SECONDARY CLAIM) SDS | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| molecular_formula | C11 H20 O |  | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | shop.bcfragrance.com |
| molecular_weight | 168.2796 | 168.2796 g/mol | RETAILER (SECONDARY CLAIM) | LIKELY_MATCH | VALID | shop.bcfragrance.com |
| additive_cas | 120-51-4 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| additive_cas | 77-93-0 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |
| additive_cas | 128-37-0 |  | RETAILER (SECONDARY CLAIM) | AMBIGUOUS | NEEDS_REVIEW | shop.perfumersapprentice.com |

**Evidencia de dosis:** 0.1-2% (MANUFACTURER, www.symrise.com, VALID)
**Evidencia de performance:** vapour_pressure=.04 hPa (0.04 hPa) (RETAILER (SECONDARY CLAIM) SDS, NEEDS_REVIEW); vapour_pressure=04 hPa (RETAILER (SECONDARY CLAIM) SDS, NEEDS_REVIEW); tenacity=Lasts > 400 hours on a smelli… (RETAILER (SECONDARY CLAIM), CONFLICT); tenacity=380 Hours (RETAILER (SECONDARY CLAIM), CONFLICT); substantivity_application=Moderate (RETAILER (SECONDARY CLAIM), VALID)
**SDS/CLP (por SDS, sin mezclar):** ningún SDS del producto analizado

**Conflictos (ningún valor sobrescrito; todos los claims conservados)**

- `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only] — valores: 89 C [OFFICIAL_MANUFACTURER]; 60 C [SECONDARY]
- `tenacity`: tenacity: independent sources disagree beyond tolerance ('rel', 0.5) — valores: Lasts > 400 hours on a smelling strip. [RETAILER]; 380 Hours [RETAILER]

**Cambios propuestos:** 8 (NEEDS_REVIEW: 6, BLOCKED_CONFLICT: 2)

- `NEEDS_REVIEW` · DOSE EVIDENCE STRUCTURED · APPEND_ROW · dose_type=SUPPLIER_RECOMMENDATION, value_text=0.1-2%, unit=%
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=logP_supplier, value=4.12, unit=log10
- `NEEDS_REVIEW` · PHYSICOCHEMICAL DATA · APPEND_ROW · property=flash_point, value=89.0, unit=C
- `BLOCKED_CONFLICT` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=>400.0, unit=hours
- `BLOCKED_CONFLICT` · PERFORMANCE EVIDENCE · APPEND_ROW · property=tenacity_on_blotter_supplier, value=380.0, unit=hours
- `NEEDS_REVIEW` · MATERIAL IDENTITY · UPDATE_CELL · resolved_cas: None → 1337-83-3
- `NEEDS_REVIEW` · MATERIAL IDENTITY · UPDATE_CELL · identity_tier: D_FAMILY_LEVEL_ONLY → B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK
- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=PARTIAL

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/ingredients-compendium/intreleven-aldehyde/): recuperar manualmente y re-ejecutar la extracción.
- Sin SDS del producto analizable: pedir SDS al proveedor/escuela.
- Resolver conflicto en `flash_point`: flash_point: independent sources disagree beyond tolerance ('abs', 6) [lower-tier dissent only]
- Resolver conflicto en `tenacity`: tenacity: independent sources disagree beyond tolerance ('rel', 0.5)
- 4 documento(s) de identidad ambigua esperan revisión humana.

---

## S-0508 — AMBROCEMOR EXT

*Grupo piloto:* DIFFICULT · *Qué prueba:* expected no-result, NO_PUBLIC_DATA_FOUND path
*Estado final:* **NO_PUBLIC_DATA_FOUND** — no usable public data in this targeted pass (not exhaustive)
*Master antes:* tier `D_FAMILY_LEVEL_ONLY`, CAS `None`, readiness 0 (NOT_READY)
*Readiness estimado después:* solo AUTO_ELIGIBLE → 0 (NOT_READY); si se aprueban también los NEEDS_REVIEW → 0 (NOT_READY)

**Queries realizadas**

- `claude_websearch` · Ambrocemor → 9 resultados
- `claude_websearch` · Ambrocemor IFF → 10 resultados
- `claude_websearch` · Ambrocemor CAS → 10 resultados
- `claude_websearch` · Ambrocemor safety data sheet → 9 resultados
- `claude_websearch` · Ambrocemor perfumery ambergris → 9 resultados
- `claude_websearch` · Ambrocemor use level → 9 resultados
- `claude_websearch` · "Ambrocenide" OR "Ambrocemor" fragrance ingredient → 9 resultados
- `claude_websearch` · "Ambrocemor Ext" → 9 resultados
- `claude_websearch` · Ambermor EX IFF CAS composition → 10 resultados
- `pubchem_api` · name:ambrocemor → 0 resultados

**Fuentes encontradas:** 64 URLs distintas; 20 seleccionadas para descarga (FETCHED: 12, ROBOTS_DISALLOWED: 3, MANUAL_RETRIEVAL_REQUIRED: 5); 14 documentos analizados (incluye APIs PubChem/PMC).

**Requieren recuperación manual (no se evadió ningún bloqueo):**

- https://cosmetics.specialchem.com/product/i-iff-ambermor — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://cosmetics.specialchem.com/product/i-iff-ambermor-dl — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.iff.com/scent/ingredients-compendium/ambermor/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/ingredients-compendium/ambermor-ex/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.specialchem.com/cosmetics/product/iff-ambermor-ex — ROBOTS_DISALLOWED (robots.txt itself returns 401/403 (site blocks automated clients) -> MANUAL_RETRIEVAL_REQ…)
- https://www.chemicalbook.com/msds/ambrox-dl.pdf — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 429 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/ingredients-compendium/ambermor-ketal-crystal/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))
- https://www.iff.com/scent/ingredients-compendium/ambermor-ketal-ipm/ — MANUAL_RETRIEVAL_REQUIRED (domain blocked earlier in run: HTTP 403 (site refuses automated access; not bypassed))

**Fuentes aceptadas**

_Ninguna._

**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**

- [Ambroxol for the treatment of COVID-19 among hospitalized patients: A…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=9582747&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)
- [Ambroxol - Resurgence of an old molecule as an anti-inflammatory agen…](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=2893422&rettype=xml) — peer-reviewed article; species NOT found; REFERENCE_COMPOSITION only (research sample, not the school bottle)

**Fuentes rechazadas:** 12

- Kao Specialties Americas LLC — official manufacturer domain (Kao); neither trade name nor CAS found
- SAFETY DATA SHEET — neither trade name nor CAS found
- Ambrocenide | — neither trade name nor CAS found
- Ambrocenide 10% in DPG | — neither trade name nor CAS found
- AMBERMOR IFF — neither trade name nor CAS found
- Material Safety Data Sheet (MSDS) — neither trade name nor CAS found
- EP4685139A2 - Neue formen von ambrocenid® - Google Patents — page is about another trade product ('A2 - Neue formen von ambrocenid'); neither trade name nor CAS found
- SAFETY DATA SHEET — neither trade name nor CAS found
- Ambrocenide (211299-54-6) – Premium Synthetic Ingredient for Perfumer… — neither trade name nor CAS found
- Ambermor EX from IFF-Aromatic Chemicals – Bulkaroma — neither trade name nor CAS found
- Safety data sheet - Wikipedia — neither trade name nor CAS found
- Ambroxan and Cetalox Differences - Blog — Scentspiracy — neither trade name nor CAS found

**Confianza de identidad:** sin fuente aceptada

**Campos descubiertos (claims)**

| campo | valor bruto | normalizado | evidencia | identidad | validación | dominio |
|---|---|---|---|---|---|---|
| gcms_study | Ambroxol for the treatment of COVID-19 among hospitalized patients: A… |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |
| gcms_study | Ambroxol - Resurgence of an old molecule as an anti-inflammatory agen… |  | PUBLISHED | AMBIGUOUS | NEEDS_REVIEW | eutils.ncbi.nlm.nih.gov |

**Evidencia de dosis:** ninguna encontrada
**Evidencia de performance:** ninguna encontrada
**SDS/CLP (por SDS, sin mezclar):** ningún SDS del producto analizado

**Cambios propuestos:** 1 (NEEDS_REVIEW: 1)

- `NEEDS_REVIEW` · INDIVIDUAL RESEARCH LOG · APPEND_ROW · search_outcome=SEARCHED_NO_USABLE_DATA

**Preguntas abiertas**

- Página oficial bloqueada a acceso automatizado (https://www.iff.com/scent/ingredients-compendium/ambermor/): recuperar manualmente y re-ejecutar la extracción.
- Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.
- Sin SDS del producto analizable: pedir SDS al proveedor/escuela.
- 2 documento(s) de identidad ambigua esperan revisión humana.

---
