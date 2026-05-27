# Setup do Repositório Depo

## ⚙️ Configuração Inicial

### 1. Clonar o Repositório

```bash
git clone https://github.com/Diogo-Pereira-Ribeiro/Depo.git
cd Depo
```

### 2. Configurar gradle.properties

O ficheiro `gradle.properties` **não está no repositório** por questões de segurança (contém endpoints privados).

**Criar o ficheiro localmente:**

```bash
cp gradle.properties.example gradle.properties
```

**Editar `gradle.properties` e preencher com os teus valores privados:**

```properties
MEGACLOUD_API=https://script.google.com/macros/s/[YOUR_API_KEY]/exec
KISSKH_API=https://script.google.com/macros/s/[YOUR_API_KEY]/exec?id=
KISSKH_SUB_API=https://script.google.com/macros/s/[YOUR_API_KEY]/exec?id=
KAISVA=https://your-api-endpoint.com
```

> ⚠️ **IMPORTANTE:** Nunca commites `gradle.properties` - está no `.gitignore`

### 3. Build das Extensões

```bash
./gradlew build
```

## 🔒 Segurança

- `gradle.properties` é ignorado pelo git - nunca será exposto
- Endpoints de API são mantidos privados e locais
- Usar `gradle.properties.example` como template

## 📥 Usar no Aniyomi

Adiciona esta URL no Aniyomi (Definições > Navegador > Repositórios):

```
https://raw.githubusercontent.com/Diogo-Pereira-Ribeiro/Depo/repo-public/index.min.json
```

## 🚀 Automação

A branch `repo-public` é atualizada automaticamente via GitHub Actions sempre que `index.min.json` for modificada na `main`.

