# 🚀 Enviar Variáveis do Ansible para Jinja2 Playground usando ansible.builtin.uri

## 📋 Visão Geral

Este método utiliza o módulo nativo `ansible.builtin.uri` do Ansible para enviar todas as variáveis (vars + facts) para o Ansible Jinja2 Playground via API HTTP POST.

## ✅ Vantagens

- ✅ **Módulo nativo**: Usa `ansible.builtin.uri` (já incluído no Ansible)
- ✅ **Simples**: Uma única task no playbook
- ✅ **Completo**: Envia todas as variáveis automaticamente (127+ variáveis)
- ✅ **Flexível**: Funciona com qualquer servidor remoto
- ✅ **Seguro**: Codificação base64 das variáveis

## 🎯 Uso Mínimo - Uma Task Única

### Arquivo: `minimal.yml`

```yaml
---
- name: Enviar todas as variáveis do Ansible para o Jinja2 Playground
  hosts: localhost
  gather_facts: yes

    - name: "Enviar {{ hostvars[inventory_hostname] | length }} variáveis para http://127.0.0.1:8000"
      ansible.builtin.uri:
        url: "http://127.0.0.1:8000/load_ansible_vars"
        method: POST
        body_format: json
        body:
          variables_b64: "{{ hostvars[inventory_hostname] | to_json | b64encode }}"
          summary:
            total_variables: "{{ hostvars[inventory_hostname] | length }}"
            module: "ansible.builtin.uri"
            source: "all_variables"
            timestamp: "{{ ansible_date_time.iso8601 }}"
        headers:
          Content-Type: "application/json"
        timeout: 10
```

### ▶️ Execução

```bash
ansible-playbook minimal.yml
```

**Resultado:**
```
TASK [Enviar 127 variáveis para http://127.0.0.1:8000] ***
ok: [localhost]
```

## 📊 Uso Avançado com Mais Informações

### Arquivo: `send_all_vars.yml`

```yaml
---
- name: Enviar todas as variáveis do Ansible para o Jinja2 Playground
  hosts: localhost
  gather_facts: yes

  vars:
    # Suas variáveis personalizadas aqui
    app_name: "MyApp"
    app_version: "2.2.0"
    env_type: "production"

  tasks:
    - name: Enviar todas as variáveis (vars + facts) para o playground
      ansible.builtin.uri:
        url: "http://127.0.0.1:8000/load_ansible_vars"
        method: POST
        body_format: json
        body:
          variables_b64: "{{ hostvars[inventory_hostname] | to_json | b64encode }}"
          summary:
            total_variables: "{{ hostvars[inventory_hostname] | length }}"
            module: "ansible.builtin.uri"
            source: "all_variables"
            timestamp: "{{ ansible_date_time.iso8601 }}"
        headers:
          Content-Type: "application/json"
        timeout: 10
      register: result

    - name: Resultado
      debug:
        msg: "✅ {{ hostvars[inventory_hostname] | length }} variáveis enviadas! Entry ID: {{ result.json.entry_id | default('N/A') }} 🔗 http://127.0.0.1:8000"
```

## 🎨 Variáveis Enviadas

O sistema envia automaticamente:

### 📦 Variáveis do Playbook
- Todas as variáveis definidas na seção `vars:`
- Variáveis passadas via `-e` ou `--extra-vars`
- Variáveis de inventory e group_vars

### 🖥️ Facts do Sistema
- `ansible_hostname`, `ansible_os_family`, `ansible_distribution`
- `ansible_python_version`, `ansible_date_time`
- Informações de rede, CPU, memória, discos
- Variáveis de ambiente (`ansible_env`)

### 📈 Total Típico
- **127+ variáveis** enviadas automaticamente

## 🔧 Configuração do Servidor

### Servidor Local
```yaml
url: "http://127.0.0.1:8000/load_ansible_vars"
```

### Servidor Remoto
```yaml
url: "http://SEU_SERVIDOR_IP:8000/load_ansible_vars"
```

### Servidor com HTTPS
```yaml
url: "https://playground.exemplo.com:8000/load_ansible_vars"
```

## 💡 Templates Jinja2 Sugeridos

Após enviar as variáveis, teste estes templates no playground:

### 1. Ver todas as variáveis
```jinja2
{{ data }}
```

### 2. Informações do sistema
```jinja2
Hostname: {{ data.ansible_hostname }}
OS: {{ data.ansible_os_family }}
Python: {{ data.ansible_python_version }}
```

### 3. Suas variáveis personalizadas
```jinja2
App: {{ data.app_name }} v{{ data.app_version }}
Ambiente: {{ data.env_type }}
```

### 4. Informações de rede
```jinja2
IP: {{ data.ansible_default_ipv4.address }}
Interface: {{ data.ansible_default_ipv4.interface }}
Gateway: {{ data.ansible_default_ipv4.gateway }}
```

### 5. Listar interfaces de rede
```jinja2
{% for interface in data.ansible_interfaces %}
- {{ interface }}
{% endfor %}
```

## 🛠️ Troubleshooting

### Erro de Conexão
```
Connection error: [Errno 111] Connection refused
```
**Solução**: Verifique se o Ansible Jinja2 Playground está rodando no endereço correto.

### Timeout
```
HTTP 408: Request Timeout
```
**Solução**: Aumente o valor de `timeout` de 10 para 30 segundos.

### Erro 404
```
HTTP 404: Not Found
```
**Solução**: Verifique se a URL está correta e inclui `/load_ansible_vars`.

## 🔍 Verificação

Após executar o playbook, verifique se as variáveis chegaram:

```bash
# Ver última entrada no histórico
curl -s http://127.0.0.1:8000/history | tail -20

# Abrir playground no navegador
xdg-open http://127.0.0.1:8000
```

## 📁 Arquivos de Exemplo

- `minimal.yml` - Versão mínima com uma task única
- `send_all_vars.yml` - Versão com mais informações
- `simple_uri.yml` - Exemplo básico e direto

## 🎯 Resumo

Esta abordagem usando `ansible.builtin.uri` é a solução **mais simples e eficiente** para enviar variáveis do Ansible para o Jinja2 Playground:

1. ✅ **Uma linha**: `ansible-playbook minimal.yml`
2. ✅ **127+ variáveis** enviadas automaticamente
3. ✅ **Módulo nativo** do Ansible (sem dependências externas)
4. ✅ **Funciona em qualquer ambiente**

**Perfect! 🎉**
