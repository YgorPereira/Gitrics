# Fluxo de login com GitHub (OAuth2)

```mermaid
flowchart TD
    A["Client<br/>(frontend Gitrics)"] -->|"1. GET /login/github"| B["Server<br/>(backend Gitrics)"]
    B -->|"2. Redireciona para autorização"| C["Github<br/>(Authorization Server)"]
    C -->|"3. Exibe tela de permissões"| D["Usuário<br/>(Resource Owner)"]

    D -->|"4a. Autoriza"| E["Github processa"]
    D -->|"4b. Nega"| F["Github retorna erro"]

    E -->|"5. Redirect + Authorization Code"| B
    B -->|"6. Troca code por token"| C
    C -->|"7. Access Token"| B

    B -->|"8. GET /user (com Access Token)"| C
    C -->|"9. Retorna perfil (id, email, nome, avatar)"| B

    B -->|"10. Busca usuário por github_id"| G[("Banco de dados")]
    G -->|"11a. Usuário não existe"| H["Cria novo usuário"]
    G -->|"11b. Usuário já existe"| I["Atualiza dados (opcional)"]

    H --> J["Server cria sessão/JWT"]
    I --> J
    J -->|"12. Retorna sessão/JWT"| A

    F -->|"error=access_denied"| B
    B -->|"401 - login cancelado"| A

    style D fill:#fff4e6
    style E fill:#e6f7ff
    style F fill:#ffe6e6
    style G fill:#f0f0f0
    style H fill:#e6ffe6
    style I fill:#e6f0ff
```

## Passos

## Passos

1. **Client → Server**: usuário clica em "Entrar com GitHub", frontend chama `/login/github`.
2. **Server → Usuário**: redireciona o navegador do usuário para a tela de autorização do GitHub.
3. **Usuário decide**: autoriza ou não o acesso.
4. **Se autoriza**: GitHub redireciona de volta ao Server com um `Authorization Code`.
5. **Server → GitHub**: troca o código por um `Access Token` (chamada server-to-server, com `client_secret`).
6. **Server → GitHub**: usa o `Access Token` para buscar o perfil do usuário (`GET /user`), obtendo `github_id`, e-mail, nome e avatar.
7. **Server → Banco de dados**: busca um usuário existente por `github_id`.
8. **Se não existe**: cria um novo registro de usuário com os dados vindos do GitHub.
9. **Se já existe**: opcionalmente atualiza campos como avatar, nome ou último login.
10. **Server → Client**: cria sessão/JWT e responde ao frontend que o login foi concluído.
11. **Se o usuário recusa**: GitHub redireciona com erro (`error=access_denied`); o Server responde com `401` ao Client.
