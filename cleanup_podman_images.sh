#!/bin/bash

# Script para limpeza de imagens Podman sem repositório definido
# Autor: Ansible Jinja2 Playground Team
# Data: $(date +%Y-%m-%d)

set -euo pipefail

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Função para mostrar uso
show_usage() {
    echo "🧹 Podman Image Cleanup Script"
    echo ""
    echo "Uso: $0 [opções]"
    echo ""
    echo "Opções:"
    echo "  -h, --help          Mostra esta ajuda"
    echo "  -d, --dry-run       Mostra o que seria removido sem executar"
    echo "  -f, --force         Remove sem confirmação"
    echo "  -a, --all-dangling  Remove todas as imagens dangling (sem tag)"
    echo "  -u, --unused        Remove imagens não utilizadas"
    echo "  -s, --stats         Mostra estatísticas de uso de espaço"
    echo ""
    echo "Exemplos:"
    echo "  $0                  # Remove imagens <none> com confirmação"
    echo "  $0 -d               # Preview das imagens que seriam removidas"
    echo "  $0 -f               # Remove sem perguntar"
    echo "  $0 -a               # Remove todas as imagens dangling"
    echo "  $0 -u               # Remove imagens não utilizadas"
}

# Função para mostrar estatísticas
show_stats() {
    log_info "Estatísticas do Podman:"
    echo ""
    
    # Total de imagens
    total_images=$(podman images -q | wc -l)
    echo "📊 Total de imagens: $total_images"
    
    # Imagens sem repositório (<none>)
    none_images=$(podman images --filter "dangling=true" -q | wc -l)
    echo "🗑️  Imagens <none>: $none_images"
    
    # Espaço total usado
    total_size=$(podman system df --format "{{.Size}}" | head -1)
    echo "💾 Espaço total usado: $total_size"
    
    # Espaço recuperável
    reclaimable=$(podman system df --format "{{.Reclaimable}}" | head -1)
    echo "♻️  Espaço recuperável: $reclaimable"
    
    echo ""
}

# Função para listar imagens sem repositório
list_none_images() {
    log_info "Buscando imagens sem repositório definido..."
    
    # Buscar imagens com <none> no repositório
    none_images=$(podman images --filter "dangling=true" --format "{{.ID}} {{.Repository}} {{.Tag}} {{.Size}}" 2>/dev/null || true)
    
    if [ -z "$none_images" ]; then
        log_success "Nenhuma imagem sem repositório encontrada!"
        return 1
    fi
    
    echo ""
    log_warning "Imagens sem repositório encontradas:"
    echo "IMAGE ID     REPOSITORY    TAG     SIZE"
    echo "--------     ----------    ---     ----"
    echo "$none_images"
    echo ""
    
    # Contar quantas imagens
    image_count=$(echo "$none_images" | wc -l)
    log_warning "Total: $image_count imagem(s) sem repositório"
    
    return 0
}

# Função para remover imagens sem repositório
remove_none_images() {
    local dry_run=$1
    local force=$2
    
    # Obter IDs das imagens dangling
    image_ids=$(podman images --filter "dangling=true" -q 2>/dev/null || true)
    
    if [ -z "$image_ids" ]; then
        log_success "Nenhuma imagem para remover!"
        return 0
    fi
    
    image_count=$(echo "$image_ids" | wc -l)
    
    if [ "$dry_run" = "true" ]; then
        log_info "🔍 DRY RUN - As seguintes imagens SERIAM removidas:"
        for id in $image_ids; do
            echo "  - $id"
        done
        log_info "Total que seria removido: $image_count imagem(s)"
        return 0
    fi
    
    # Confirmar remoção se não for force
    if [ "$force" = "false" ]; then
        echo ""
        read -p "❓ Remover $image_count imagem(s) sem repositório? [y/N]: " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Operação cancelada pelo usuário"
            return 0
        fi
    fi
    
    # Remover imagens
    log_info "🗑️ Removendo $image_count imagem(s)..."
    
    removed_count=0
    failed_count=0
    
    for id in $image_ids; do
        if podman rmi "$id" 2>/dev/null; then
            log_success "Removida: $id"
            ((removed_count++))
        else
            log_error "Falha ao remover: $id"
            ((failed_count++))
        fi
    done
    
    echo ""
    log_success "✨ Limpeza concluída!"
    log_info "📊 Resumo: $removed_count removida(s), $failed_count falha(s)"
}

# Função para remover imagens não utilizadas
remove_unused_images() {
    local dry_run=$1
    local force=$2
    
    if [ "$dry_run" = "true" ]; then
        log_info "🔍 DRY RUN - Imagens não utilizadas que SERIAM removidas:"
        podman image prune --dry-run
        return 0
    fi
    
    if [ "$force" = "false" ]; then
        echo ""
        read -p "❓ Remover todas as imagens não utilizadas? [y/N]: " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Operação cancelada pelo usuário"
            return 0
        fi
    fi
    
    log_info "🗑️ Removendo imagens não utilizadas..."
    podman image prune -f
    log_success "✨ Limpeza de imagens não utilizadas concluída!"
}

# Função principal
main() {
    local dry_run=false
    local force=false
    local all_dangling=false
    local unused=false
    local show_help=false
    local show_statistics=false
    
    # Parse argumentos
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help=true
                shift
            ;;
            -d|--dry-run)
                dry_run=true
                shift
            ;;
            -f|--force)
                force=true
                shift
            ;;
            -a|--all-dangling)
                all_dangling=true
                shift
            ;;
            -u|--unused)
                unused=true
                shift
            ;;
            -s|--stats)
                show_statistics=true
                shift
            ;;
            *)
                log_error "Opção desconhecida: $1"
                echo ""
                show_usage
                exit 1
            ;;
        esac
    done
    
    # Mostrar ajuda se solicitado
    if [ "$show_help" = "true" ]; then
        show_usage
        exit 0
    fi
    
    # Mostrar estatísticas se solicitado
    if [ "$show_statistics" = "true" ]; then
        show_stats
        exit 0
    fi
    
    # Verificar se podman está disponível
    if ! command -v podman &> /dev/null; then
        log_error "Podman não encontrado! Instale o Podman primeiro."
        exit 1
    fi
    
    echo "🧹 Podman Image Cleanup Script"
    echo "=============================="
    
    # Mostrar estatísticas iniciais
    show_stats
    
    # Executar limpeza baseada nos parâmetros
    if [ "$unused" = "true" ]; then
        remove_unused_images "$dry_run" "$force"
        elif [ "$all_dangling" = "true" ]; then
        remove_none_images "$dry_run" "$force"
    else
        # Comportamento padrão: listar e remover imagens <none>
        if list_none_images; then
            remove_none_images "$dry_run" "$force"
        fi
    fi
    
    # Mostrar estatísticas finais se não for dry run
    if [ "$dry_run" = "false" ]; then
        echo ""
        log_info "Estatísticas após limpeza:"
        show_stats
    fi
}

# Verificar se está sendo executado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
  echo "  -a, --all-dangling  Remove todas as imagens dangling (sem tag)"
  echo "  -u, --unused        Remove imagens não utilizadas"
  echo "  -s, --stats         Mostra estatísticas de uso de espaço"
  echo ""
  echo "Exemplos:"
  echo "  $0                  # Remove imagens <none> com confirmação"
  echo "  $0 -d               # Preview das imagens que seriam removidas"
  echo "  $0 -f               # Remove sem perguntar"
  echo "  $0 -a               # Remove todas as imagens dangling"
  echo "  $0 -u               # Remove imagens não utilizadas"
}

# Função para mostrar estatísticas
show_stats() {
  log_info "Estatísticas do Podman:"
  echo ""

  # Total de imagens
  total_images=$(podman images -q | wc -l)
  echo "📊 Total de imagens: $total_images"

  # Imagens sem repositório (<none>)
  none_images=$(podman images --filter "dangling=true" -q | wc -l)
  echo "🗑️  Imagens <none>: $none_images"

  # Espaço total usado
  total_size=$(podman system df --format "{{.Size}}" | head -1)
  echo "💾 Espaço total usado: $total_size"

  # Espaço recuperável
  reclaimable=$(podman system df --format "{{.Reclaimable}}" | head -1)
  echo "♻️  Espaço recuperável: $reclaimable"

  echo ""
}

# Função para listar imagens sem repositório
list_none_images() {
  log_info "Buscando imagens sem repositório definido..."

  # Buscar imagens com <none> no repositório
  none_images=$(podman images --filter "dangling=true" --format "{{.ID}} {{.Repository}} {{.Tag}} {{.Size}}" 2>/dev/null || true)

  if [ -z "$none_images" ]; then
    log_success "Nenhuma imagem sem repositório encontrada!"
    return 1
  fi

  echo ""
  log_warning "Imagens sem repositório encontradas:"
  echo "IMAGE ID     REPOSITORY    TAG     SIZE"
  echo "--------     ----------    ---     ----"
  echo "$none_images"
  echo ""

  # Contar quantas imagens
  image_count=$(echo "$none_images" | wc -l)
  log_warning "Total: $image_count imagem(s) sem repositório"

  return 0
}

# Função para remover imagens sem repositório
remove_none_images() {
  local dry_run=$1
  local force=$2

  # Obter IDs das imagens dangling
  image_ids=$(podman images --filter "dangling=true" -q 2>/dev/null || true)

  if [ -z "$image_ids" ]; then
    log_success "Nenhuma imagem para remover!"
    return 0
  fi

  image_count=$(echo "$image_ids" | wc -l)

  if [ "$dry_run" = "true" ]; then
    log_info "🔍 DRY RUN - As seguintes imagens SERIAM removidas:"
    for id in $image_ids; do
      echo "  - $id"
    done
    log_info "Total que seria removido: $image_count imagem(s)"
    return 0
  fi

  # Confirmar remoção se não for force
  if [ "$force" = "false" ]; then
    echo ""
    read -p "❓ Remover $image_count imagem(s) sem repositório? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      log_info "Operação cancelada pelo usuário"
      return 0
    fi
  fi

  # Remover imagens
  log_info "🗑️ Removendo $image_count imagem(s)..."

  removed_count=0
  failed_count=0

  for id in $image_ids; do
    if podman rmi "$id" 2>/dev/null; then
      log_success "Removida: $id"
      ((removed_count++))
    else
      log_error "Falha ao remover: $id"
      ((failed_count++))
    fi
  done

  echo ""
  log_success "✨ Limpeza concluída!"
  log_info "📊 Resumo: $removed_count removida(s), $failed_count falha(s)"
}

# Função para remover imagens não utilizadas
remove_unused_images() {
  local dry_run=$1
  local force=$2

  if [ "$dry_run" = "true" ]; then
    log_info "🔍 DRY RUN - Imagens não utilizadas que SERIAM removidas:"
    podman image prune --dry-run
    return 0
  fi

  if [ "$force" = "false" ]; then
    echo ""
    read -p "❓ Remover todas as imagens não utilizadas? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      log_info "Operação cancelada pelo usuário"
      return 0
    fi
  fi

  log_info "🗑️ Removendo imagens não utilizadas..."
  podman image prune -f
  log_success "✨ Limpeza de imagens não utilizadas concluída!"
}

# Função principal
main() {
  local dry_run=false
  local force=false
  local all_dangling=false
  local unused=false
  local show_help=false
  local show_statistics=false

  # Parse argumentos
  while [[ $# -gt 0 ]]; do
    case $1 in
      -h|--help)
        show_help=true
        shift
        ;;
      -d|--dry-run)
        dry_run=true
        shift
        ;;
      -f|--force)
        force=true
        shift
        ;;
      -a|--all-dangling)
        all_dangling=true
        shift
        ;;
      -u|--unused)
        unused=true
        shift
        ;;
      -s|--stats)
        show_statistics=true
        shift
        ;;
      *)
        log_error "Opção desconhecida: $1"
        echo ""
        show_usage
        exit 1
        ;;
    esac
  done

  # Mostrar ajuda se solicitado
  if [ "$show_help" = "true" ]; then
    show_usage
    exit 0
  fi

  # Mostrar estatísticas se solicitado
  if [ "$show_statistics" = "true" ]; then
    show_stats
    exit 0
  fi

  # Verificar se podman está disponível
  if ! command -v podman &> /dev/null; then
    log_error "Podman não encontrado! Instale o Podman primeiro."
    exit 1
  fi

  echo "🧹 Podman Image Cleanup Script"
  echo "=============================="

  # Mostrar estatísticas iniciais
  show_stats

  # Executar limpeza baseada nos parâmetros
  if [ "$unused" = "true" ]; then
    remove_unused_images "$dry_run" "$force"
  elif [ "$all_dangling" = "true" ]; then
    remove_none_images "$dry_run" "$force"
  else
    # Comportamento padrão: listar e remover imagens <none>
    if list_none_images; then
      remove_none_images "$dry_run" "$force"
    fi
  fi

  # Mostrar estatísticas finais se não for dry run
  if [ "$dry_run" = "false" ]; then
    echo ""
    log_info "Estatísticas após limpeza:"
    show_stats
  fi
}

# Verificar se está sendo executado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
