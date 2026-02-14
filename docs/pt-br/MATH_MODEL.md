# BIP: 888 (Proposto) - Modelo Matemático

🌐 [English](../../MATH_MODEL.md) | 🇧🇷 **Português (Brasil)**

Este documento define as equações fundamentais que regem a geração de decoys (fantasmas) e a análise de entropia para o protocolo BIP 888.

---

## 1. Geração de Decoys via Mapas Caóticos

A segurança do ESS baseia-se na geração de $N$ transações falsas ($T_{decoy}$) que são indistinguíveis da transação real ($T_{real}$) para um observador sem a chave de tempo.

Utilizamos o **Mapa Logístico** como gerador de números pseudo-aleatórios determinísticos (PRNG) devido à sua sensibilidade às condições iniciais (efeito borboleta).

### Equação do Mapa Logístico:
$$x_{n+1} = r \cdot x_n \cdot (1 - x_n)$$

Onde:
- $x_n$: O estado atual (normalizado entre 0 e 1).
- $x_n$: O estado atual (normalizado entre 0 e 1).
- $r$: O parâmetro de crescimento (para comportamento caótico, $r \approx 4.0$, especificamente $r = 3.999...$).

### Aplicação na Geração de Decoys:
Para cada transação $T_{real}$:

1.  **Semente ($Seed$):**
    $$S = Hash(T_{real} \parallel Nonce_{rede} \parallel TimeSlot)$$
    Essa semente é convertida para um valor inicial $x_0 \in (0, 1)$.

2.  **Iteração Caótica:**
    O sistema itera o mapa logístico $K$ vezes para eliminar transientes.
    $$x_k = f^{(K)}(x_0)$$

3.  **Geração dos Atributos do Decoy:**
    Para cada $T_{decoy_i}$ ($i$ de 1 a $N$):
    - O valor $x_{k+i}$ é usado para derivar os atributos da transação falsa (destinatário, valor, locktime).
    - Ex: $Valor_{decoy} = (x_{k+i} \cdot MaxBTC) \mod (Valor_{real} \pm \delta)$

Isso garante que os decoys tenham propriedades estatísticas "orgânicas" e não pareçam ruído branco uniforme.

## 2. Análise de Entropia (Grover vs. Swarm)

### Otimização de Grover:
Um computador quântico usando o Algoritmo de Grover pode encontrar uma chave em $\mathcal{O}(\sqrt{N})$ operações.
Para uma chave de $b$ bits, o espaço de busca é $2^b$. Grover reduz para $\sqrt{2^b} = 2^{b/2}$.

### Impacto do Enxame (Swarm):
Se o atacante precisa distinguir entre $1$ real e $M$ decoys antes de tentar quebrar a chave.

O espaço de busca efetivo se torna:
$$Espaço_{total} = (M + 1) \cdot 2^b$$

O tempo de ataque quântico ($T_{attack}$) se torna:
$$T_{attack} \propto \sqrt{(M + 1) \cdot 2^b} = \sqrt{M+1} \cdot 2^{b/2}$$

### Ganho de Segurança ($\Delta S$):
O fator de aumento de segurança é $\sqrt{M}$.
- Se $M = 10.000$ (10 mil decoys), o tempo de ataque aumenta em $\sqrt{10.000} = 100$ vezes.
- Se $M = 1.000.000$ (1 milhão de decoys), o tempo aumenta em $1.000$ vezes.

Isso significa que para manter a mesma probabilidade de sucesso, o atacante precisaria de $1.000$ vezes mais qubits coerentes ou tempo de coerência.

## 4. Cenários de Implementação (Grover vs. SHA-256)

A eficácia do ESS depende do custo real de execução do **Oráculo SHA-256** dentro de um CRQC (Computador Quântico Relevante para Criptografia). Definimos dois cenários para análise de segurança:

### Cenário A: Pessimista (Hardware Quântico Avançado)
- **Suposição**: Portas quânticas de alta fidelidade e correção de erro eficiente permitem uma execução compacta do SHA-256.
- **Custo do Oráculo ($C_{oracle}$)**: $\approx 10^9$ operações quânticas elementares por iteração.
- **Resultado**: Com $M = 10^5$, o tempo de busca total $T_{total} = \sqrt{M} \cdot C_{oracle}$ ainda se mantém acima de 600s para hardwares de primeira geração.

### Cenário B: Otimista (Limites Físicos Próximos)
- **Suposição**: A decoerência limita a profundidade do circuito quântico, forçando uma implementação mais "pesada" do SHA-256.
- **Custo do Oráculo ($C_{oracle}$)**: $\approx 25 \cdot 10^9$ operações.
- **Resultado**: A segurança do ESS é amplificada significativamente; o "Enxame" torna o custo de cada tentativa proibitivo, garantindo que mesmo ataques paralelos falhem em bater o tempo de 600s do Hashrate Global.

---

## 5. Escalonabilidade e Relay

### Compactação de Decoys
Para mitigar o overhead de largura de banda, o protocolo utiliza a função geradora caótica para enviar apenas o par $\{Hash(T_{real}), \text{Semente}\}$ em vez dos dados completos de $10.000$ transações. Os nós regeneram o enxame localmente para fins de obfuscação de scan.

---

## 6. Análise de Entropia da Semente

A segurança do sistema depende da imprevisibilidade da Semente $S$. Definimos a entropia da semente $H(S)$ como:

$$H(S) = H(Bloco_{prev}) + H(Nonce_{node}) + H(TimeSlot)$$

- **$H(Bloco_{prev})$**: Entropia fornecida pelo Proof-of-Work (~80 bits de segurança min-entropy).
- **$H(Nonce_{node})$**: Entropia local do nó, desconhecida pelo atacante remoto.

Para um atacante prever a distribuição exata do enxame em um tempo $t < 600s$, ele precisaria quebrar a função de hash SHA-256 para encontrar colisões que gerassem a mesma semente, o que é computacionalmente inviável mesmo para CRQC neste intervalo de tempo.

---

*"A autenticidade desta proposta reside na sua capacidade matemática de sobreviver ao caos."*

## 📜 Licenciamento
Este documento e o modelo matemático são contribuições técnicas de **Éve Sk > CapGorack**. 
Distribuído sob a **Licença BSD de 2 Cláusulas**.
Copyright © 2026 Éve Sk > CapGorack.
