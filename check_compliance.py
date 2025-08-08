#!/usr/bin/env python3
"""
Script para verificar conformidade com as regras do .copilotrc
"""

import os
import re
import yaml
import sys

def load_copilotrc():
  """Carrega as regras do .copilotrc"""
  try:
    with open('.copilotrc', 'r') as f:
      return yaml.safe_load(f)
  except Exception as e:
    print(f"❌ Erro ao ler .copilotrc: {e}")
    return None

def check_coding_style():
  """Verifica se o coding style está sendo seguido"""
  print("🎨 Verificando coding style...")

  issues = []

  # Verifica arquivos Python
  for root, dirs, files in os.walk('.'):
    # Ignora diretórios específicos
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__']]

    for file in files:
      if file.endswith('.py'):
        file_path = os.path.join(root, file)

        with open(file_path, 'r', encoding='utf-8') as f:
          lines = f.readlines()

        for i, line in enumerate(lines, 1):
          # Verifica trailing whitespace (linha não pode terminar com espaços ou tabs)
          if line.endswith(' ') or line.endswith('\t'):
            issues.append(f"   ⚠️  {file_path}:{i} - Trailing whitespace")

          # Verifica indentação (deve ser múltiplo de 2)
          leading_spaces = len(line) - len(line.lstrip(' '))
          if leading_spaces > 0 and leading_spaces % 2 != 0:
            issues.append(f"   ⚠️  {file_path}:{i} - Indentação incorreta (não é múltiplo de 2)")

  if issues:
    print("   ❌ Problemas encontrados:")
    for issue in issues[:10]:  # Mostra apenas os primeiros 10
      print(issue)
    if len(issues) > 10:
      print(f"   ... e mais {len(issues) - 10} problemas")
  else:
    print("   ✅ Coding style OK")

  return len(issues) == 0

def check_test_structure():
  """Verifica se a estrutura de testes está correta"""
  print("🧪 Verificando estrutura de testes...")

  if not os.path.exists('tests'):
    print("   ❌ Diretório tests não encontrado")
    return False

  test_files = [f for f in os.listdir('tests') if f.startswith('test_') and f.endswith('.py')]

  if len(test_files) == 0:
    print("   ❌ Nenhum arquivo de teste encontrado")
    return False

  print(f"   ✅ Encontrados {len(test_files)} arquivos de teste:")
  for test_file in test_files:
    print(f"      📄 {test_file}")

  return True

def check_documentation():
  """Verifica se a documentação está presente"""
  print("📚 Verificando documentação...")

  required_docs = ['README.md', 'USAGE.md', 'INSTALL.md', 'LOOP_USAGE.md']
  missing_docs = []

  for doc in required_docs:
    if not os.path.exists(doc):
      missing_docs.append(doc)

  if missing_docs:
    print("   ❌ Documentação faltando:")
    for doc in missing_docs:
      print(f"      📄 {doc}")
    return False
  else:
    print("   ✅ Documentação completa")
    return True

def main():
  print("🔍 Verificando conformidade com .copilotrc")
  print("=" * 50)

  # Carrega configurações
  config = load_copilotrc()
  if not config:
    sys.exit(1)

  print("✅ Arquivo .copilotrc carregado com sucesso")
  print()

  # Executa verificações
  results = []
  results.append(check_coding_style())
  results.append(check_test_structure())
  results.append(check_documentation())

  print()
  print("=" * 50)

  if all(results):
    print("🎉 TODAS AS VERIFICAÇÕES PASSARAM!")
    print("✅ Projeto está em conformidade com .copilotrc")
    sys.exit(0)
  else:
    print("⚠️  ALGUMAS VERIFICAÇÕES FALHARAM")
    print("❌ Projeto precisa de ajustes para conformidade")
    sys.exit(1)

if __name__ == "__main__":
  main()
