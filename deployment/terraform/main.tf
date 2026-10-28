# Esqueleto de infraestructura para un clúster de Raspberry Pi.
# Requiere el provider de tu plataforma de virtualización o nube.

terraform {
  required_version = ">= 1.6"
}

variable "nodos" {
  description = "Número de nodos del clúster"
  type        = number
  default     = 3
}

variable "memoria_por_nodo_gb" {
  description = "RAM por nodo"
  type        = number
  default     = 16
}

output "resumen_cluster" {
  value = {
    nodos        = var.nodos
    ram_total_gb = var.nodos * var.memoria_por_nodo_gb
    arquitectura = "arm64"
  }
}
