# Criptografía

Este repositorio contiene apuntes de criptografía y utilidades programadas en *Python*, que pueden resultar útiles para aprender y comprender los distintos conceptos criptográficos.

**IMPORTANTE: Estos scripts no deben usarse para proyectos reales que precisen encriptar datos. Para ello es recomendable utilizar bibliotecas contrastadas y auditadas por parte de la comunidad y/o expertos en criptografía.** Por otro lado, el desarrollo de estos *scripts* no busca la eficiencia, sino ayudar a comprender el funcionamiento de los distintos conceptos, con lo que su ejecución puede ser mucho más lenta que la de bibliotecas y utilidades realizadas con la eficiencia en mente, y programadas en lenguajes compilados, mucho más veloces.

## Tabla de contenidos

1. [Álgebra para criptografía](capitulos/algebra.md)
1. [Problema del logaritmo discreto](capitulos/logaritmo-discreto.md)
1. [Números primos](capitulos/primos.md)
1. [Hashing](capitulos/hashing.md)
1. [RSA](capitulos/rsa.md)
1. [Criptografía de Curva Elíptica](capitulos/curva-eliptica.md)
1. [Firma digital](capitulos/firma.md)
1. [BIP-39](capitulos/bip39.md)
1. [BIP-32 (y BIP-44)](capitulos/bip32.md)

## Scripts

> Esta sección contiene una breve descripción de la funcionalidad de los *scripts*. Las explicaciones teóricas pueden encontrarse en los capítulos correspondientes.

### [utils.py](utils.py)

Funciones útiles para los demás *scripts*.

### [primos.py](primos.py)

Utilidades relacionadas con el cálculo de números primos grandes. Necesario, por ejemplo, para el cálculo de las claves del algoritmo *RSA*. Permite generar en disco la relación de los primeros primos.

### [sha2_hashing.py](sha2_hashing.py)

*Secure Hash Algorithm*. Utilidades para calcular *digests* (*hashes*) mediante los algoritmos de la familia *SHA-2*. Se implementan 4 de ellos: *SHA-224*, *SHA-256*, *SHA-384* y *SHA-512*.

### [ripemd_hashing.py](ripemd_hashing.py)

Utilidades para calcular *digests* con el algoritmo *RIPEMD-160*.

### [rsa.py](rsa.py)

Utilidades para calcular pares de claves y trabajar con el algoritmo de encriptación de clave pública *RSA*.

### [ce.py](ce.py)

Utilidades relacionadas con la **criptografía de curva elíptica**.

### [firma.py](firma.py)

Funciones relacionadas con la firma digital.

### [bip39.py](bip39.py)

Explora el [Bitcoin Improvement Proposal 39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki), relativo a la *seed phrase* y la semilla para la generación de monederos. Utiliza la *wordlist* oficial en inglés, almacenada en el archivo ***wordlist.json***.

### [bip32.py](bip32.py)

Funciones relativas al [Bitcoin Improvement Proposal 32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki), relativo a la generación de monederos jerárquicos deterministas, a partir de una semilla (como la originada en *BIP-39*).
