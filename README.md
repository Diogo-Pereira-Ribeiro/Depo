# Depo - Extensões de Anime para Aniyomi

Repositório com extensões de anime para o **Aniyomi**.

## 📥 Como Adicionar ao Aniyomi

1. Abra o Aniyomi
2. Vá para **Definições > Navegador > Repositórios de Extensões**
3. Clique em **+** para adicionar um novo repositório
4. Cole a URL abaixo:

```
https://raw.githubusercontent.com/Diogo-Pereira-Ribeiro/Depo/main/index.min.json
```

5. Confirme e as extensões estarão disponíveis para instalar

## 📦 Extensões Disponíveis

Veja o ficheiro `index.json` para a lista completa de extensões e suas fontes.

Repositório de extensões de anime para o [Aniyomi](https://github.com/aniyomiorg/aniyomi).

## 📦 Instalação

Adiciona este repositório ao Aniyomi:

```
https://raw.githubusercontent.com/Diogo-Pereira-Ribeiro/Depo/repo/index.min.json
```

## 🏗️ Estrutura

- **`src/`** - Extensões por idioma (ex: `src/pt` para português)
- **`lib/`** - Bibliotecas reutilizáveis (extractors, interceptors)
- **`lib-multisrc/`** - Temas multi-fonte
- **`core/`** - Utilitários compartilhados

## 🔨 Build Local

Para compilar e gerar o índice localmente:

```powershell
# Build com limpeza anterior
.\build-local.ps1 -CleanBuild

# Build simples
.\build-local.ps1

# Gera: repo/, index.json, index.min.json, repo.json
```

## 🚀 CI/CD

O repositório usa **GitHub Actions** para:
1. Compilar automaticamente as extensões a cada push
2. Gerar o `index.min.json`
3. Fazer push para branch `repo` (acessível publicamente)

Workflow: `.github/workflows/build-and-publish.yml`

## 🔗 Ficheiros Gerados

- **`index.min.json`** - Índice minificado (usado pela app)
- **`index.json`** - Índice formatado (debug)
- **`repo.json`** - Metadados do repositório
- **`repo/apk/`** - APKs compilados
- **`repo/icon/`** - Ícones das extensões

## 📝 Notas

- As extensões compiladas ficam no branch `repo`
- O código-fonte fica no branch `main`
- O link `index.min.json` atualiza automaticamente após cada push
