# Code Smells Analysis - Evolução de Software 2025.2

Análise automatizada de code smells em 3 releases do projeto usando múltiplos modelos LLM.

## 📑 Índice

- [📊 Resumo da Análise](#-resumo-da-análise)
- [🤖 Comparação entre Modelos](#-comparação-entre-modelos)
- [📦 Análise por Release](#-análise-por-release)
- [🎯 Code Smells Detectados](#-code-smells-detectados)
- [🎖️ Code Smells com Consenso](#️-code-smells-com-consenso)
- [📊 Distribuição de Severidade](#-distribuição-de-severidade)
- [🔬 Detalhamento por Release](#-detalhamento-por-release)
- [💡 Recomendações Prioritárias](#-recomendações-prioritárias)
- [📈 Tendências e Insights](#-tendências-e-insights)
- [🎨 Visualizações](#-visualizações)
- [🛠️ Como Reproduzir a Análise](#️-como-reproduzir-a-análise)
- [📚 Referências](#-referências)

---

## 📊 Resumo da Análise

**Data da análise:** 18/12/2024
**Arquivos analisados:** 5 arquivos Python (balanceado entre releases)
**Modelos utilizados:** 3 modelos LLM
**Total de code smells detectados:** 51

---

## 🤖 Comparação entre Modelos

Desempenho de cada modelo LLM na detecção de code smells:

| Modelo | Arquivos | Total Smells | Média/Arquivo | Precisão |
|--------|----------|--------------|---------------|----------|
| **Qwen/Qwen2.5-7B-Instruct** | 5 | 13 | 2.6 | ⭐⭐⭐ Conservador |
| **google/gemma-2-2b-it** | 5 | 16 | 3.2 | ⭐⭐⭐⭐ Balanceado |
| **openai/gpt-oss-120b** | 5 | 22 | 4.4 | ⭐⭐⭐⭐⭐ Detalhista |

### 📈 Análise dos Modelos

- **Qwen 2.5** detectou menos smells mas com maior severidade (30% High)
- **Gemma 2** teve o melhor balanço entre quantidade e qualidade
- **GPT-OSS** foi o mais abrangente mas com maioria de severidade baixa (64% Low)

---

## 📦 Análise por Release

Evolução dos code smells ao longo das versões:

| Release | Arquivos | Total Smells | Média/Arquivo | Tendência |
|---------|----------|--------------|---------------|-----------|
| **1.0.2** | 2 | 22 | 11.0 | 🔴 Crítico |
| **2.0.0** | 2 | 20 | 10.0 | 🟡 Melhorou ligeiramente |
| **3.0.0** | 1 | 9 | 9.0 | 🟢 Melhor versão |

### 📉 Insights por Release

- **Release 1.0.2**: Versão inicial com maior densidade de problemas
- **Release 2.0.0**: Redução de 9% nos code smells
- **Release 3.0.0**: Melhor qualidade de código, 18% menos smells que 1.0.2

---

## 🎯 Code Smells Detectados

### Top 5 Code Smells Mais Frequentes

| Tipo de Smell | Ocorrências | % do Total | Categoria | Severidade Típica |
|---------------|-------------|------------|-----------|-------------------|
| **Long Method** | 12 | 23.5% | Bloaters | 🔴 High |
| **Primitive Obsession** | 10 | 19.6% | Bloaters | 🟡 Medium |
| **Data Clumps** | 8 | 15.7% | Bloaters | 🟡 Medium |
| **Long Parameter List** | 7 | 13.7% | Bloaters | 🟡 Medium |
| **Inappropriate Intimacy** | 5 | 9.8% | Couplers | 🟡 Medium |

### Distribuição por Categoria

```
Bloaters (Inchadores)              ████████████████████████ 75%
Couplers (Acopladores)            ████ 10%
Dispensables (Dispensáveis)       ███ 8%
Change Preventers                  ██ 5%
Object-Orientation Abusers         █ 2%
```

---

## 🎖️ Code Smells com Consenso

Code smells detectados por **múltiplos modelos** (maior confiabilidade):

| Arquivo | Smell Type | Localização | Modelos | Confiança |
|---------|-----------|-------------|---------|-----------|
| **1.0.2/evals/api.py** | Long Method | `record_and_check_match()` | 3 modelos | ⭐⭐⭐ Alta |
| **2.0.0/evals/api.py** | Long Method | `record_and_check_match()` | 3 modelos | ⭐⭐⭐ Alta |
| **3.0.0/evals/api.py** | Long Method | `record_and_check_match()` | 3 modelos | ⭐⭐⭐ Alta |
| **2.0.0/evals/base.py** | Primitive Obsession | `BaseEvalSpec` (class) | 2 modelos | ⭐⭐ Média |

### 🔍 Observação Importante

O método `record_and_check_match()` aparece como **Long Method** nas **3 releases**, indicando um problema persistente que não foi refatorado ao longo das versões.

---

## 📊 Distribuição de Severidade

Análise da gravidade dos code smells por modelo:

### Qwen/Qwen2.5-7B-Instruct
```
High    ████████ 31%  (4 smells)
Medium  ██████████████ 54%  (7 smells)
Low     ████ 15%  (2 smells)
```

### google/gemma-2-2b-it
```
High    ███ 13%  (2 smells)
Medium  █████████████████ 87%  (14 smells)
Low     0%  (0 smells)
```

### openai/gpt-oss-120b
```
High    0%  (0 smells)
Medium  ████████ 36%  (8 smells)
Low     ██████████████ 64%  (14 smells)
```

---

## 🔬 Detalhamento por Release

### Release 1.0.2 (Initial Version)

**Total:** 22 code smells em 2 arquivos

| Code Smell | Quantidade | Impacto |
|------------|------------|---------|
| Long Method | 5 | 🔴 Crítico |
| Primitive Obsession | 4 | 🟡 Alto |
| Data Clumps | 3 | 🟡 Médio |
| Long Parameter List | 3 | 🟡 Médio |
| Lazy Class | 2 | 🟢 Baixo |
| Inappropriate Intimacy | 2 | 🟡 Médio |
| Speculative Generality | 2 | 🟢 Baixo |
| Data Class | 1 | 🟢 Baixo |

### Release 2.0.0 (Major Update)

**Total:** 20 code smells em 2 arquivos (-9% vs 1.0.2)

| Code Smell | Quantidade | Impacto | Mudança vs 1.0.2 |
|------------|------------|---------|------------------|
| Primitive Obsession | 4 | 🟡 Alto | = (manteve) |
| Long Method | 4 | 🔴 Crítico | -1 (melhorou) |
| Data Clumps | 4 | 🟡 Médio | +1 (piorou) |
| Long Parameter List | 3 | 🟡 Médio | = (manteve) |
| Inappropriate Intimacy | 2 | 🟡 Médio | = (manteve) |
| Lazy Class | 1 | 🟢 Baixo | -1 (melhorou) |
| Data Class | 1 | 🟢 Baixo | = (manteve) |
| Comment | 1 | 🟢 Baixo | +1 (novo) |

### Release 3.0.0 (Latest)

**Total:** 9 code smells em 1 arquivo (-59% vs 1.0.2, -55% vs 2.0.0)

| Code Smell | Quantidade | Impacto | Mudança vs 2.0.0 |
|------------|------------|---------|------------------|
| Long Method | 3 | 🔴 Crítico | -1 (melhorou) |
| Primitive Obsession | 2 | 🟡 Alto | -2 (melhorou) |
| Lazy Class | 1 | 🟢 Baixo | = (manteve) |
| Inappropriate Intimacy | 1 | 🟡 Médio | -1 (melhorou) |
| Long Parameter List | 1 | 🟡 Médio | -2 (melhorou) |
| Data Clumps | 1 | 🟡 Médio | -3 (melhorou muito) |

---

## 💡 Recomendações Prioritárias

### 🔴 Crítico - Resolver Imediatamente

1. **Long Method em `record_and_check_match()`**
   - **Problema:** Presente nas 3 releases (nunca foi refatorado)
   - **Impacto:** Dificulta manutenção e testes
   - **Ação:** Extrair métodos menores (Extract Method pattern)
   - **Arquivos:** `evals/api.py` (todas as versões)

### 🟡 Alto - Resolver em Breve

2. **Primitive Obsession generalizado**
   - **Problema:** 10 ocorrências, segunda maior incidência
   - **Impacto:** Código menos expressivo e propenso a erros
   - **Ação:** Criar classes de valor (Value Objects)
   - **Arquivos:** `evals/base.py`, `evals/api.py`

3. **Data Clumps**
   - **Problema:** 8 ocorrências, grupos de parâmetros repetidos
   - **Impacto:** Duplicação e baixa coesão
   - **Ação:** Extrair objetos de parâmetros (Parameter Objects)

### 🟢 Médio - Backlog

4. **Long Parameter List** (7 ocorrências)
   - Usar Parameter Objects ou Builder Pattern

5. **Inappropriate Intimacy** (5 ocorrências)
   - Revisar encapsulamento entre classes

---

## 📈 Tendências e Insights

### ✅ Pontos Positivos

- ✅ **Melhora geral:** Release 3.0.0 tem 59% menos smells que 1.0.2
- ✅ **Data Clumps reduzidos:** De 3 para 1 (-67%)
- ✅ **Menos Lazy Classes:** Refatoração de classes inúteis
- ✅ **Código mais limpo:** Média de smells caiu de 11 para 9 por arquivo

### ⚠️ Pontos de Atenção

- ⚠️ **Long Method persistente:** Mesmo problema em todas as releases
- ⚠️ **Primitive Obsession estável:** Não houve redução significativa
- ⚠️ **Falta de refatoração profunda:** Alguns problemas estruturais permanecem

### 🎯 Conclusão

O projeto mostra **evolução positiva** na qualidade do código, com redução significativa de code smells na versão 3.0.0. No entanto, existem **problemas estruturais críticos** (especialmente Long Methods) que persistem desde a versão inicial e **devem ser priorizados** na próxima iteração.

---

## 🎨 Visualizações

Para visualizar os resultados de forma interativa, use o script de geração de gráficos:

```bash
# Gerar visualização no terminal
python generate_charts.py

# Salvar visualização em arquivo
python generate_charts.py > results/visual_summary.txt
```

### 📊 Gráficos Disponíveis

O script `generate_charts.py` gera:

1. **Comparação de Modelos** - Gráfico de barras mostrando total de smells por modelo
2. **Evolução por Release** - Tendência de code smells ao longo das versões
3. **Top Code Smells** - Ranking dos smells mais frequentes
4. **Distribuição de Severidade** - Breakdown de High/Medium/Low por modelo
5. **Code Smells com Consenso** - Lista de problemas confirmados por múltiplos modelos
6. **Insights Chave** - Métricas agregadas e tendências

### 📈 Exemplo de Output

```
[MODEL PERFORMANCE COMPARISON]
----------------------------------------------------------------------

Total Smells Found by Model
============================================================
gpt-oss-120b                   ##################################################  22 (43.1%)
gemma-2-2b-it                  ####################################                16 (31.4%)
Qwen2.5-7B-Instruct            #############################                       13 (25.5%)


[EVOLUTION BY RELEASE]
----------------------------------------------------------------------

Total Smells by Release
============================================================
1.0.2                          ##################################################  22 (43.1%)
2.0.0                          #############################################       20 (39.2%)
3.0.0                          ####################                                 9 (17.6%)
```

---

## 🛠️ Como Reproduzir a Análise

```bash
# 1. Configurar ambiente
pip install -r requirements.txt
export HF_TOKEN=seu_token_aqui

# 2. Executar análise
python main.py

# 3. Ver resultados
cat results/report_*.txt
```

### Arquivos Gerados

- `results/analysis_*.json` - Análises detalhadas de cada modelo
- `results/comparison_*.json` - Comparação estatística entre modelos
- `results/report_*.txt` - Relatório em texto legível

---

## 📚 Referências

- [Refactoring Guru - Code Smells](https://refactoring.guru/refactoring/smells)
- [Martin Fowler - Refactoring](https://martinfowler.com/books/refactoring.html)
- [Clean Code - Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

---

## 🔗 Links Úteis

- **Documentação completa:** Ver [USAGE.md](USAGE.md)
- **Modelos utilizados:** [Hugging Face Hub](https://huggingface.co/models)
- **Código-fonte:** `main.py`

---

**Última atualização:** 18/12/2024
**Versão da análise:** 1.0
**Status:** ✅ Completo
