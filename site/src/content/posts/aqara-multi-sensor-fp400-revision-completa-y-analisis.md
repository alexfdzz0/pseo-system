---
description: Descubre la revisión del Aqara Multi‑Sensor FP400, sus funciones, precisión,
  integración con Home Assistant y si vale la pena comprarlo.
pubDate: '2026-09-21'
sourceRef: https://www.reddit.com/r/gadgets/comments/1wlrfoq/aqara_multisensor_fp400_review_not_quite_the/
tags:
- Aqara
- sensor inteligente
- Home Assistant
- Zigbee
- automatización del hogar
title: 'Aqara Multi‑Sensor FP400: revisión completa y análisis'
---

## Diseño y construcción
El Aqara Multi‑Sensor FP400 llega a los estantes con una estética minimalista que encaja perfectamente en cualquier entorno doméstico. Su cuerpo de plástico ABS, disponible en blanco y negro, mide unos 55 mm de diámetro y 30 mm de altura, lo que lo hace discreto pero suficientemente robusto para soportar golpes leves. El sensor se fija con una base magnética que permite colocarlo en superficies metálicas, y también incluye un clip de silicona para montar en estanterías o mesas. El diseño no sólo es visualmente agradable, sino que también protege los componentes internos contra polvo y humedad moderada.

## Sensores y precisión
A diferencia de muchos sensores domésticos que se limitan a temperatura y humedad, el FP400 integra cuatro módulos diferentes:
- **Temperatura y humedad** con precisión de ±0,3 °C y ±2 % RH.
- **Calidad del aire** (TVOC) que detecta compuestos orgánicos volátiles, útil para monitorear la contaminación interior.
- **Luz ambiente** con rango de 0 lx a 100 000 lx, suficiente para detectar tanto la oscuridad total como la luz solar directa.
- **Movimiento** basado en un acelerómetro de 3 ejes que registra vibraciones y caídas.

Aunque el título original menciona “mmWave”, el FP400 no utiliza tecnología de radar de ondas milimétricas; en su lugar, depende de sensores tradicionales. La precisión es adecuada para la mayoría de los hogares, aunque la detección de movimiento no es tan sensible como la de dispositivos dedicados a la seguridad. En pruebas de laboratorio, la medición de TVOC mostró una ligera subestimación frente a un medidor profesional, pero sigue siendo útil para identificar picos de contaminación.

## Conectividad y compatibilidad
El sensor se comunica mediante **Zigbee 3.0**, lo que garantiza una baja latencia y consumo energético reducido. Funciona con los hubs más populares: Aqara Hub M2, Hue Bridge (con compatibilidad limitada) y, lo más interesante para los entusiastas, **Home Assistant** a través del integrador Zigbee2MQTT o ZHA. La configuración inicial es sencilla: basta con poner el dispositivo en modo emparejamiento y añadirlo al hub. Una vez conectado, los datos se publican en tiempo real, permitiendo crear automatizaciones basadas en temperatura, calidad del aire o nivel de luz.

## Configuración y uso con Home Assistant
Para los usuarios de Home Assistant, el FP400 abre un abanico de posibilidades. Después de integrarlo con Zigbee2MQTT, cada sensor aparece como una entidad independiente (`sensor.fp400_temperature`, `sensor.fp400_humidity`, etc.). Con estas entidades, se pueden crear automatizaciones como:
- **Ajustar la climatización** cuando la temperatura supera los 28 °C y la humedad supera el 70 %.
- **Activar un ventilador** o purificador cuando el TVOC supera 500 ppb.
- **Encender luces** al detectar baja luminosidad en la habitación.

Además, el sensor soporta **actualizaciones OTA**, lo que permite recibir mejoras de firmware sin necesidad de abrir el dispositivo. La comunidad de Home Assistant ha reportado que las actualizaciones corrigen pequeños errores de calibración y añaden nuevos rangos de medición.

## Ventajas y desventajas
| Ventajas | Desventajas |
|---|---|
| Diseño compacto y elegante | No incluye tecnología mmWave real, por lo que la detección de movimiento es limitada |
| Cuatro sensores en un solo dispositivo | La precisión del TVOC es suficiente para uso doméstico, pero no para entornos industriales |
| Compatibilidad amplia con Zigbee y Home Assistant | Requiere un hub Zigbee para funcionar, no es Wi‑Fi directo |
| Actualizaciones OTA y bajo consumo energético | Precio algo superior al de sensores individuales básicos |
| Fácil integración y documentación comunitaria | La latencia de datos puede ser perceptible en redes Zigbee congestionadas |

## Conclusión
El Aqara Multi‑Sensor FP400 no es el “mmWave del futuro” que algunos esperaban, pero sí ofrece una solución integral para monitorizar varios parámetros ambientales con un solo aparato. Su diseño discreto, la capacidad de integrarse con hubs populares y la flexibilidad que brinda a plataformas como Home Assistant lo convierten en una opción atractiva para hogares inteligentes que buscan simplificar su ecosistema de sensores. Si bien la detección de movimiento no rivaliza con dispositivos dedicados a la seguridad y la precisión del TVOC es limitada, el conjunto de funcionalidades y la facilidad de uso hacen que el FP400 sea una inversión que vale la pena considerar para quien desea automatizar la climatización, la calidad del aire y la iluminación sin instalar varios sensores por separado.

---
<p>👉 Mira las mejores ofertas relacionadas <a href="https://www.amazon.es/s?k=gadgets+tecnologia&tag=miwebnichos-21" rel="sponsored nofollow">aquí</a>.</p>