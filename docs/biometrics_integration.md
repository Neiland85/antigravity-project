# 🧬 Biometría Multiplataforma: Integración de Huella Dactilar

Este documento detalla la estrategia de integración para sistemas de detección de huella dactilar en el ecosistema Antigravity, cubriendo dispositivos móviles (Android/iOS), tablets (iPad) y terminales de sobremesa (Windows/macOS/Linux).

## 1. Abstracción del Hardware y Sensores
Para soportar "todo tipo de terminal", debemos abstraer los tres tipos principales de sensores:
- **Ópticos:** Toman una foto de alta resolución.
- **Capacitivos:** Midgen la capacitancia eléctrica para mapear crestas.
- **Ultrasónicos (Avanzado):** Usan ondas de sonido para un mapa 3D (ej. Qualcomm 3D Sonic). Estos son los más seguros ante falsificaciones.

## 2. Implementación por Sistema Operativo

### 📱 Móvil (Android / iOS)
- **iOS / iPadOS:** Usar el framework `LocalAuthentication`.
  - *Context*: `LAContext`.
  - *Policy*: `.deviceOwnerAuthenticationWithBiometrics`.
- **Android:** Usar `BiometricPrompt` (AndroidX Biometric Library).
  - Soporta autenticación unificada (Huella, Rostro, Iris) con un fallback seguro al KeyStore.

### 💻 Sobremesa (Desktop)
- **Windows:** Integración con **Windows Hello** mediante el Windows Biometric Framework (WBF).
- **macOS:** Framework `LocalAuthentication` (similar a iOS) para dispositivos con Touch ID.
- **Linux:** Interfaz con `fprintd` y módulos PAM.

## 3. Web & Cross-Platform (WebAuthn)
Para que Antigravity funcione en navegadores de cualquier dispositivo sin importar el SO, implementaremos **WebAuthn (FIDO2)**.
- Permite que el navegador pida al SO la validación biométrica.
- El servidor de Antigravity valida una firma criptográfica en lugar de recibir el dato de la huella (Privacidad Total).

## 4. Arquitectura de Seguridad (The Secure Enclave)
Los datos de la huella **NUNCA** deben salir del dispositivo.
1. El sensor captura la huella.
2. El **TEE (Trusted Execution Environment)** o **Secure Enclave** procesa la imagen.
3. Se genera un token de éxito/fallo o un desafío firmado.
4. El servicio **Sentinel** en Antigravity recibe la confirmación criptográfica.

## 5. Próximos Pasos de Implementación
1. **Módulo Sentinel-Bio:** Crear un endpoint en Sentinel para registrar "Bio-Keys" vinculadas a usuarios.
2. **Bridge React Native / Flutter:** (Si se desarrolla app móvil) Implementar el wrapper para los sensores.
3. **WebAuthn Demo:** Implementar un dashboard de login biométrico en el frontend actual.

---
¿Por qué plataforma te gustaría empezar a ver código de implementación? (ej. el backend en Sentinel para WebAuthn o el wrapper para Android/iOS?)
