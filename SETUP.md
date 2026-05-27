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

**Editar `gradle.properties` e preencher com os teus valores:**

```properties
MEGACLOUD_API=https://script.google.com/macros/s/[YOUR_KEY]/exec
KISSKH_API=https://script.google.com/macros/s/[YOUR_KEY]/exec?id=
KISSKH_SUB_API=https://script.google.com/macros/s/[YOUR_KEY]/exec?id=
KAISVA=https://api.example.com
```

> ⚠️ **IMPORTANTE:** Nunca commitës `gradle.properties` - está no `.gitignore`

### 3. Build das Extensões

```bash
./gradlew build
```

## 🔒 Segurança

- `gradle.properties` é ignorado pelo git
- Endpoints de API são mantidos privados
- Usar `gradle.properties.example` como template

## 📝 Documentação

- [README.md](README.md) - Instruções para o Aniyomi
- [.github/workflows/](\.github/workflows) - Automação CI/CD
