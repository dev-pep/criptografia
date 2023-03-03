# Firma digital

Una firma digital tiene dos utilidades: por un lado, garantizar la autenticidad del mensaje, y por otro asegurar que el mensaje lo ha generado (lo ha firmado) un remitente determinado.

## Idea general

La idea es la siguiente: Alice redacta un mensaje M. Luego genera un hash de dicho mensaje H(M), y encripta ese hash con su clave privada: E(H(M)), que es precisamente la firma digital (o firma electrónica). Luego envia el mensaje M (en claro) y la firma. Bob recibe ambas cosas y desencripta la firma utilizando la clave pública de Alice, obteniendo el hash del mensaje H(M). Como también tiene el mensaje, lo pasa a su vez por la función hash y compara los dos hashes. Si coinciden, el mensaje es auténtico y además proviende de Alice.

## DSA

Para ver el funcionamiento del algoritmo *DSA* (*Digital Signature Algorithm*) véase el código fuente en ***firma.py***.
