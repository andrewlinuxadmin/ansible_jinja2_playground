#!/bin/bash

# Script simples para limpeza rápida de imagens Podman dangling
# Uso: ./quick_cleanup_podman.sh

echo "🧹 Limpeza Rápida de Imagens Podman"
echo "===================================="

# Verificar se podman está disponível
if ! command -v podman &> /dev/null; then
    echo "❌ Podman não encontrado!"
    exit 1
fi

# Mostrar estatísticas antes
echo "📊 Antes da limpeza:"
podman system df

echo ""
echo "🗑️  Removendo imagens dangling..."

# Remover imagens dangling (sem tag)
podman image prune -f

echo ""
echo "🗑️  Removendo containers parados..."

# Remover containers parados
podman container prune -f

echo ""
echo "🗑️  Removendo volumes não utilizados..."

# Remover volumes não utilizados
podman volume prune -f

echo ""
echo "📊 Após a limpeza:"
podman system df

echo ""
echo "✅ Limpeza concluída!"
