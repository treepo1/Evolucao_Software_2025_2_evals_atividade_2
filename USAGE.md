# Guia de Uso - Análise de Code Smells com LLMs

Este sistema utiliza 3 modelos de linguagem do Hugging Face para detectar code smells em código Python baseado na taxonomia do [Refactoring Guru](https://refactoring.guru/refactoring/smells).

## 📋 Pré-requisitos

1. **Python 3.8+**
2. **Token do Hugging Face**
   - Acesse: https://huggingface.co/settings/tokens
   - Crie um token de acesso (Read)

## 🚀 Instalação

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar token do Hugging Face
export HF_TOKEN=seu_token_aqui

# Ou no Windows:
set HF_TOKEN=seu_token_aqui
```

## 📖 Como Usar

### Execução Básica

```bash
python main.py
```

Por padrão, o script analisa os primeiros 5 arquivos Python da pasta `releases/`.

### Analisar Todos os Arquivos

Edite `main.py` e modifique a linha:

```python
analyzer.run_analysis(
    releases_dir=releases_dir,
    sample_size=None  # None = todos os arquivos
)
```

### Analisar Quantidade Específica

```python
analyzer.run_analysis(
    releases_dir=releases_dir,
    sample_size=10  # Analisa 10 arquivos
)
```

## 🤖 Modelos Utilizados

O sistema usa 3 modelos por padrão:

1. **Qwen/Qwen2.5-7B-Instruct** - Modelo multilíngue da Alibaba
2. **meta-llama/Llama-3.2-3B-Instruct** - Modelo da Meta
3. **mistralai/Mistral-7B-Instruct-v0.3** - Modelo da Mistral AI

Para alterar os modelos, edite a lista `MODELS` em `main.py`:

```python
MODELS = [
    "seu-modelo/aqui",
    "outro-modelo/aqui",
    "terceiro-modelo/aqui"
]
```

## 📊 Resultados Gerados

O sistema gera 3 arquivos na pasta `results/`:

### 1. `analysis_TIMESTAMP.json`
Resultados brutos de cada modelo para cada arquivo analisado.

**Estrutura:**
```json
{
  "success": true,
  "model": "nome-do-modelo",
  "file": "path/arquivo.py",
  "analysis": {
    "file_analyzed": "path/arquivo.py",
    "total_smells_found": 3,
    "smells": [
      {
        "smell_type": "Long Method",
        "category": "Bloaters",
        "location": {...},
        "evidence": "código aqui...",
        "severity": "High",
        "justification": "explicação...",
        "refactoring_suggestion": "sugestão...",
        "refactored_example": "exemplo..."
      }
    ]
  }
}
```

### 2. `comparison_TIMESTAMP.json`
Comparação estatística entre os modelos.

**Contém:**
- Estatísticas por modelo (total de smells, distribuição por tipo, severidade)
- Code smells com consenso (detectados por múltiplos modelos)
- Matriz de concordância entre modelos

### 3. `report_TIMESTAMP.txt`
Relatório em texto legível com:
- Estatísticas gerais
- Desempenho de cada modelo
- Code smells encontrados com consenso

## 🔍 Code Smells Detectados

O sistema busca code smells em 5 categorias:

### 1. Bloaters (Inchadores)
- Long Method
- Large Class
- Primitive Obsession
- Long Parameter List
- Data Clumps

### 2. Object-Orientation Abusers (Abusadores de OO)
- Switch Statements
- Temporary Field
- Refused Bequest
- Alternative Classes with Different Interfaces

### 3. Change Preventers (Preventores de Mudança)
- Divergent Change
- Shotgun Surgery
- Parallel Inheritance Hierarchies

### 4. Dispensables (Dispensáveis)
- Comments
- Duplicate Code
- Lazy Class
- Data Class
- Dead Code
- Speculative Generality

### 5. Couplers (Acopladores)
- Feature Envy
- Inappropriate Intimacy
- Message Chains
- Middle Man

## ⚙️ Configurações Avançadas

### Ajustar Tamanho Máximo de Arquivo

```python
analyzer = CodeSmellAnalyzer(models=MODELS)
python_files = analyzer.read_python_files(
    directory=releases_dir,
    max_size=100000  # 100KB em caracteres
)
```

### Ajustar Timeout da API

Edite a função `query_model()`:

```python
response = requests.post(
    self.api_url,
    headers=self.headers,
    json=payload,
    timeout=120  # 120 segundos
)
```

### Ajustar Tokens de Resposta

```python
payload = {
    "model": model,
    "messages": [...],
    "temperature": 0.1,
    "max_tokens": 8192,  # Aumentar para respostas maiores
    "response_format": {"type": "json_object"}
}
```

## 🐛 Solução de Problemas

### Erro: "HF_TOKEN não encontrado"
```bash
# Verificar se variável está definida
echo $HF_TOKEN  # Linux/Mac
echo %HF_TOKEN%  # Windows

# Definir temporariamente
export HF_TOKEN=seu_token  # Linux/Mac
set HF_TOKEN=seu_token     # Windows
```

### Erro: "Failed to parse JSON response"
- O modelo pode ter retornado texto ao invés de JSON
- Verifique `raw_response` no arquivo de resultados
- Considere usar outro modelo

### Erro: "Request timeout"
- Aumente o timeout na função `query_model()`
- Reduza `max_size` dos arquivos
- Reduza `max_tokens` na requisição

### Erro: Rate limit exceeded
- A API do HuggingFace tem limites de taxa
- Adicione delays entre requisições:

```python
import time
time.sleep(2)  # Aguardar 2 segundos entre arquivos
```

## 📈 Exemplo de Saída

```
================================================================================
🔍 INICIANDO ANÁLISE DE CODE SMELLS
================================================================================

📁 Lendo arquivos Python de: releases
✅ 150 arquivos Python encontrados
📊 Limitando análise a 5 arquivos (amostra)

[1/5]
📄 Analisando: releases/3.0.0/evals/api.py
   Tamanho: 12543 caracteres
   🤖 Modelo: Qwen/Qwen2.5-7B-Instruct
      ✅ 4 code smells encontrados
   🤖 Modelo: meta-llama/Llama-3.2-3B-Instruct
      ✅ 3 code smells encontrados
   🤖 Modelo: mistralai/Mistral-7B-Instruct-v0.3
      ✅ 5 code smells encontrados

...

💾 Resultados salvos em: results/analysis_20241218_143522.json
💾 Comparação salva em: results/comparison_20241218_143522.json
📊 Relatório gerado em: results/report_20241218_143522.txt

================================================================================
✅ ANÁLISE CONCLUÍDA
================================================================================
```

## 📚 Referências

- [Refactoring Guru - Code Smells](https://refactoring.guru/refactoring/smells)
- [Hugging Face API Documentation](https://huggingface.co/docs/api-inference/)
- [Hugging Face Models](https://huggingface.co/models)
