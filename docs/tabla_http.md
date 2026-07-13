\# Tabla de códigos HTTP



| Código HTTP | Estado | Descripción | Prueba realizada |

|---|---|---|---|

| 200 | OK | Solicitud procesada correctamente | GET /dispositivos |

| 201 | Created | Recurso creado correctamente | POST /dispositivos |

| 400 | Bad Request | Solicitud incorrecta o IP duplicada | POST /dispositivos con IP repetida |

| 401 | Unauthorized | Usuario no autenticado | No implementado; mejora futura |

| 403 | Forbidden | Usuario sin permisos | No implementado; mejora futura |

| 404 | Not Found | Recurso no encontrado | GET /dispositivos/10.10.10.10 |

| 422 | Unprocessable Entity | JSON incompleto o inválido | POST /dispositivos sin campo IP |

| 500 | Internal Server Error | Error interno o fallo de conexión remota | /red/comando o /linux/comando con IP sin SSH |

