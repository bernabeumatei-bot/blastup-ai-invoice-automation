# Automatización de facturas: demo por excepciones

Demo genérica de Blastup Partner con **facturas completamente ficticias**. Lee registros JSON ya extraídos, comprueba campos básicos, fecha, importes, divisa y posibles duplicados, y separa los casos que requieren revisión humana. No usa OCR, IA, correo ni conexión a un ERP; esos pasos son posibles ampliaciones, no funciones presentes.

**Web oficial:** https://blast-up.com

## Probar

Requiere Python 3.10 o superior. Desde el directorio del repositorio, ejecuta:

    python invoice_demo.py
    python -m unittest discover -s tests

El comando imprime JSON con candidatos para exportación revisada, excepciones y resumen. No escribe archivos ni envía datos a servicios. Puedes pasar la ruta de otro JSON con una lista de facturas; no uses datos reales en esta demo pública.

## Reglas de ejemplo

- Campos obligatorios: proveedor, identificador fiscal y número de factura.
- Fecha ISO válida y divisa EUR.
- Importes numéricos no negativos; neto + impuesto debe coincidir con total con tolerancia de 0,01 €.
- Posible duplicado si coinciden identificador fiscal y número de factura dentro del lote.

Estas reglas no verifican que una factura sea auténtica, que el identificador fiscal sea válido, que el impuesto sea correcto o que proceda pagarla. Un resultado sin excepciones sigue requiriendo los controles de aprobación de la empresa. No hay datos ni flujos de clientes en este repositorio.

## English

Generic exception-based invoice intake demo by Blastup Partner. It processes entirely fictional, pre-extracted JSON records and separates basic validation exceptions from candidates for a reviewed export. It does not perform OCR, AI extraction, email ingestion, payment or ERP posting. Run python invoice_demo.py to see the example output. Passing validation never means that an invoice is authentic or approved for payment.

**Official website:** https://blast-up.com
