# 🚀 Ansible Jinja2 Playground - Demo Playbooks

Este diretório contém playbooks de demonstração que mostram o poder do **Ansible Jinja2 Playground** para
desenvolvimento de templates complexos.

> **📂 Nota**: Todos os arquivos de demonstração estão auto-contidos no diretório `ansible-jinja2-playground/`.

## 📋 Cenário Demonstrado

**Problema Real**: Você precisa criar um relatório de auditoria de servidor coletando:
- ✅ Serviços em execução
- ✅ Portas abertas
- ✅ Processos com maior uso de CPU
- ✅ Informações de memória e disco
- ✅ Dados do sistema operacional

**Desafio**: Criar um template Jinja2 complexo para consolidar tudo em um relatório profissional.

**Solução**: Use o Ansible Jinja2 Playground para desenvolver e testar o template interativamente!

## 📁 Arquivos de Demonstração

### 1. `demo_server_audit.yml` 🎯
**Playbook principal que demonstra o workflow completo:**

```bash
# Execute o playground primeiro
python run.py

# Em outro terminal, execute o demo
ansible-playbook demo_server_audit.yml
```

**O que faz:**
1. **Coleta dados** do sistema (serviços, portas, processos, etc.)
2. **Consolida** tudo em uma estrutura de dados organizada
3. **Envia automaticamente** para o Ansible Jinja2 Playground via API
4. **Fornece instruções** de como desenvolver o template
5. **Mostra exemplo básico** do relatório final

### 2. `demo_advanced_report.yml` 🏆
**Exemplo do playbook APÓS desenvolver o template no playground:**

- Mostra como usar o template desenvolvido
- Gera relatório HTML profissional com CSS
- Demonstra templates complexos com lógica condicional
- Inclui análise de segurança automatizada

## 🔄 Workflow Recomendado

### Fase 1: Coleta de Dados
```yaml
- name: Gather system information
  ansible.builtin.service_facts:
  # ... outras tasks de coleta
```

### Fase 2: Envio para Playground
```yaml
- name: Send to Ansible Jinja2 Playground
  ansible.builtin.uri:
    url: "{{ playground_url }}/load_ansible_vars"
    method: POST
    body_format: json
    body:
      input: "{{ collected_data | to_nice_json | b64encode }}"
```

### Fase 3: Desenvolvimento Interativo
1. **Abra o playground** em http://127.0.0.1:8000
2. **Selecione os dados** no dropdown "Load from History"
3. **Desenvolva o template** com feedback em tempo real
4. **Teste diferentes abordagens** (HTML, Markdown, JSON)
5. **Refine a lógica** com filters e condicionais

### Fase 4: Implementação Final
```yaml
- name: Generate final report
  ansible.builtin.template:
    src: developed_template.j2
    dest: "/path/to/report.html"
  vars:
    data: "{{ collected_data }}"
```

## 🎯 Vantagens Demonstradas

### ⚡ **Desenvolvimento Rápido**
- Sem necessidade de executar playbook completo a cada teste
- Feedback instantâneo em mudanças no template
- Ambiente isolado para experimentação

### 🔍 **Visualização de Dados**
- Veja exatamente como seus dados estão estruturados
- Teste diferentes filtros e transformações
- Validação de sintaxe em tempo real

### 🛡️ **Desenvolvimento Seguro**
- Teste templates sem afetar sistemas de produção
- Validação prévia de lógica complexa
- Iteração rápida sem riscos

### 📊 **Templates Complexos**
Os exemplos mostram como desenvolver:
- **Relatórios HTML** com CSS e tabelas
- **Análise condicional** (ex: alertas de segurança)
- **Formatação avançada** de dados
- **Loops aninhados** e filtros complexos

## 🧪 Exemplos de Templates para Testar

### Template HTML Básico:
```jinja2
<h1>Servidor: {{ hostname }}</h1>
<p>Sistema: {{ distribution }} {{ distribution_version }}</p>
<h2>Serviços Críticos:</h2>
<ul>
{% for service in services.critical_services %}
  <li>{{ service }}</li>
{% endfor %}
</ul>
```

### Template com Lógica Condicional:
```jinja2
{% set port_count = network.open_ports | length %}
{% if port_count > 20 %}
⚠️ ALERTA: Muitas portas abertas ({{ port_count }})
{% elif port_count > 10 %}
⚡ ATENÇÃO: Portas moderadas ({{ port_count }})
{% else %}
✅ SEGURO: Poucas portas abertas ({{ port_count }})
{% endif %}
```

### Template Markdown:
```jinja2
# Relatório de Auditoria: {{ hostname }}

## Resumo Executivo
- **Uptime**: {{ (uptime | int / 3600) | round(1) }}h
- **Serviços**: {{ services.running_services }}/{{ services.total_count }}
- **Memória**: {{ memtotal_mb }}MB

## Portas Abertas
{% for port in network.open_ports %}
- Porto {{ port }}
{% endfor %}
```

## 🚀 Executando os Demos

```bash
# 1. Ative o ambiente virtual (necessário)
# Use seu método preferido de ativação do ambiente virtual

# 2. Inicie o playground
python ansible-jinja2-playground/run.py

# 3. Em outro terminal, execute o demo
ansible-playbook demo_server_audit.yml

# 4. Abra o browser e desenvolva seu template
# http://127.0.0.1:8000

# 5. Veja o exemplo avançado
ansible-playbook demo_advanced_report.yml
```

## 💡 Dicas Pro

1. **Use o histórico**: Todos os dados enviados ficam salvos para reutilização
2. **Teste filtros**: Experimente `| length`, `| join`, `| select`, `| reject`
3. **Valide dados**: Use o playground para entender a estrutura exata dos dados
4. **Itere rapidamente**: Desenvolva incrementalmente, testando cada mudança
5. **Copie o resultado**: Use o template final direto no seu playbook

---

**🎉 Resultado**: Templates Jinja2 profissionais desenvolvidos em minutos, não horas!

**🔥 Produtividade**: Desenvolvimento 10x mais rápido com feedback instantâneo!
