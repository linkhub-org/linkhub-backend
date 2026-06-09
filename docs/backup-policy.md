# Política de Backup — Linkhub

## 1. O que precisa de backup

| Item | Onde fica | Criticidade |
|------|-----------|-------------|
| Banco de dados PostgreSQL | Railway (produção) | Alta |
| Variáveis de ambiente `.env` | Local / fora do repositório | Alta |
| Repositório Git | GitHub | Baixa — já versionado |

---

## 2. Banco de dados

**Frequência:** diário em produção, manual antes de cada deploy.

**Gerar backup:**
```bash
pg_dump -U postgres -d linkhub -F c -f backup_$(date +%Y%m%d).dump
```

**Restaurar:**
```bash
pg_restore -U postgres -d linkhub backup_20260101.dump
```

**Retenção:** manter os últimos 7 backups diários e 1 por sprint concluída.

**Nomenclatura:**
```
backup_20260101.dump
backup_sprint2_20260115.dump
```

---

## 3. Variáveis de ambiente

O `.env` nunca vai para o Git. Deve ser armazenado em local seguro e
compartilhado apenas entre os membros da equipe.

Opções aceitas:
- Documento privado no Notion da equipe
- Google Drive compartilhado apenas entre os desenvolvedores
- GitHub Secrets para variáveis de produção

Nunca compartilhar por WhatsApp ou e-mail sem criptografia.

---

## 4. Procedimento obrigatório antes de cada deploy

```bash
# 1. Gerar backup do banco de produção
pg_dump -U postgres -d linkhub -F c -f backup_pre_deploy_$(date +%Y%m%d).dump

# 2. Confirmar que o backup foi gerado
ls -lh backup_*.dump
```

O deploy só deve ser realizado após confirmar o backup.

---

## 5. Responsabilidades

| Ação | Responsável |
|------|-------------|
| Backup antes de deploy | Guilherme |
| Guardar `.env` de produção | Guilherme e Kaio |
| Verificar backups por sprint | Kaio |

---

## 6. Procedimento de recuperação

```
1. Parar o servidor
2. Recriar o banco vazio:  createdb linkhub
3. Restaurar o backup:     pg_restore -U postgres -d linkhub <arquivo>.dump
4. Aplicar migrations:     python manage.py migrate
5. Reiniciar o servidor
6. Executar smoke test para validar os fluxos principais
```

---

## 7. Localização dos arquivos de backup

Os arquivos `.dump` não devem ser commitados no repositório. Armazene-os
em local externo ao projeto (Google Drive, HD externo ou serviço de
armazenamento em nuvem).

Adicione ao `.gitignore`:
```
*.dump
```