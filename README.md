<div align="center">
  <h1>
  Universidade Estadual de Feira de Santana (UEFS)

  Problema 2: ZapZap
  </h1>

  <h3>
    João Gabriel Lima Almeida
  </h3>

  <p>
  DEPARTAMENTO DE TECNOLOGIA
    
  TEC502 - CONCORRÊNCIA E CONECTIVIDADE
  </p>
</div>

# 1. Introdução

<p style="text-align: justify;">
  A comunicação é um dos aspectos mais importantes para o funcionamento da sociedade. Desde a antiguidade a humanidade sempre buscou formas de se comunicar a distancia, incialmente através de mensageiros, cartas e bilhetes até posteriormente com meios mais modernos como telefones, telégrafos e etc. Com a internet não foi diferente, a comunicação rápida e de larga escalabilidade oferecida pelas redes de computadores permitiu um novo avanço: a troca de mensagens instantâneas. O surgimentos das redes sociais ampliou ainda mais esse aspecto, se tornando uma feature quase que enssencial dentro desses ambientes.
  
  Junto com esse fenomeno uma questão se torna bastante relevante: a proteção dos dados dessas conversas. Sejam conversas pessoais ou decisões importantes de empresas, a privacidade do que é transmitido através dos pacotes pela rede é essencial uma vez que esses dados circulam por diversos dispositivos até chegarem em seus destinos finais e podem ser interceptados por sniffers de rede ou outras tecnologias nos nós. Sendo assim, a criptografia se apresenta como um aspecto importante na implementação desses mensageiros.

  Outro aspecto importante, principalmente no ambito de empresas é a questão da ordenação dessas mensagens. Em uma conversa casual entre pessoas, a ordem que as mensagens chegam é importante já que ela afeta o sentido do que é dito, porém, pequenas divergencias na ordem como de mensagens enviadas "ao mesmo tempo" não são um problema tão relevante. Entretando, quando essas mensageiros estão sendo usados no ambito profissional, a divergencia de ordem nas mensagens podem causar diversos problemas, principalmetne quando elas são utilizadas para sincronizar eventos de duas ou mais partes. Por esse motivo, outro ponto relevante na questão dos chats de mensagens instantâneas é a ordenação total das mensagens nos usuários participantes.

  Pensando nisso, esse relatório descreve o desenvolvimento de um mensageiro simples de troca de mensagens instantâneas em uma rede desenvolvido para o mercado corporativo baseado no modelo peer-to-peer descentralizado que possibilite a comunicação entre usuários de um grupo de forma segura. Além disso, o sistema deve oferecer confiabilidade para garantir que todos os usuários recebam todas as mensagens na mesma ordem, mesmo aquelas que o usuário não tenha recebido por estar offiline (voluntáriamente ou por desconexão). Além disso, o protótipo deve seguir as seguintes características:
  
- Utilizar socket do tipo UDP
- Considerar o modelo de falhas, ou seja, que possa ocorrer perda de pacotes
- Solução distribuida, descentralizada
- Não utilizar relógio fisico nem medidas de tempo do gênero uma vez que são imprecisas e não confiáveis
- Não utilizar servidores de tempo

  A linguagem de programação utilizada no desenvolvimento do mensagteiro foi o Python na versão 3.12 e suas libs nativas. A metodologia do desenvolvimento utilizada foi a Problem Based Learning (PBL), onde os alunos discutiram em grupo a os passos para solucionar o problema apresentadoe e construir a aplicação com os requisitos determinados pelos tutores.
  
</p>

# 2. Desenvolvimento

<p style="text-align: justify;">
  Tendo em vista os requisitos do problema foi pensado para ser solucionado da seguinte forma: Cada usuário da rede vai executar o programa e este vai se conectar diretamente a todos os demais nós (usuários) da rede realizando trocas de pacotes peer-to-peer. Cada programa conta com 1 thread de execução principal e 3 secundárias que são executadas paralelamente. 
  
  A thread principal tem um trabalho bem objetivo e simples: pedir as informações ao usuário (quem são os pares do grupo, a chave de criptografia, etc) e enviar as mensagens do usário no momento em que ele as digitar. Pralelamente, uma thread executa o método Listner, que fica escutando uma porta através do socket para receber os pacotes enviados dos outros nós a ele, sejam mensagens ou o que for. A thread Lister não realizada nenhuma ação com os pacotes além de adiciona-los a uma lista pkgCache, um cache que guarda todos os pacotes temporáriamente. Esse cache é necessário pois durante o tempo em que uma mensagem está sendo tratada e alguma ação está sendo executada, possa ser que uma nova mensagem chegue e caso o programa não esteja aguardando ela, esse pacote será perdido. 
  
  Para tratar as mensagens uma outra thread: pkgSort. Essa thread é responsável por pegar uma a uma as mensagens do cache e dar o seu devido destino a elas. As mensagens podem ser de 3 tipos diferentes, seja uma mensagem nova, uma mensagem antiga recuperada ou uma mensagem espcial de solicitação de sincronização. Utilizando essa thread junto ao cache, o programa consegue receber e tratar de forma correta novos pacotes minimizando ao máximo a perda de pacotes, já que a thread que espera por novos dados apenas adiciona no cache e fica aguardando novos, enquanto a thread pkgSort realiza a filtragem dessa mensangens, já que ela não precisa aguradar nada.
  
  A ultima thread que é executada sozinha no programa é a eventualSync, uma thread responsável por executar solicitações de sincronização para os nós da rede para garantir que as mensagens se mantenham atualizadas. Essa solicitação é realizada de X em X tempo, sendo esse X definito em código.

  - Problemas enfrentados
  
  Um dos desafios chave desse problema é a questão da ordenação das mensagens. Manter a ordem das mensangens em todos os usuários de incio é uma tarefa dificil, afinal, devido a caracteristica da comunicação via pacotes, mesmo enviando para todos os usuários ao mesmo tempo não existe nenhuma garantia de que aquele pacote irá chegar ao mesmo tempo para todos os usuários e nenhuma outra suposição baseada em tempo. Dessa forma, a sincronia das mensagens não pode utilizar como parâmetro a ordem de chegada dos pacotes. Para resolver esse problema, foi pensado o seguinte: Cada mensagem (lembrando que: mensagem ≠ pacote) precisa ter um indice universal que indique em qual ordem ela deve ficar; cada mensagem precisa de uma forma de identificação unica, para que não exista problemas em caso de duas mensagens possuirem o mesmo indice ou mensagens duplicadas; deve haver um algorítimo unico que ordene as mensagens de forma que garanta que, independente das maquinas, as mensagens A, B, C, ... N possuam a mesma ordem em todos os nós. Dessa forma a ordenação total das mensagens consegue ser garantida.

  Outro ponto importante é que o sistema utiliza o protocolo de transporte User Datagram Protocol (UDP) que é um tipo de protocolo de troca de pacotes mais veloz e simples mas que não garante que esses datagramas vão de fato chegar ao destino e nem há nativamente nenhum tipo de confirmação da chegada (ou não). Por esse motivo, como já é requisito do problema, o sistema inteiro deve ser pensado na perspectiva de que podem haver falhas que possam comprometer a integridade do sistema, já que um pacote que não chega para um usuário faz com que ele perca uma mensagem e afeta a ordenação das demais. Para solucionar isso foi pensado que o sistema deve possuir uma forma de sincronizar as conversas locais de cada nó de forma que garanta que todos os nós vão possuir as mesmas mensagens. A solução pensanda é que periodicamente cada nó solicite para os demais que enviem suas mensagens contidas na conversa com exceção daquelas que o proprio solicitando enviou (já que é garantido que ele já as possui). Dessa forma, recebendo as mensagens das conversas antigas dos nós, o nó que está sincronizando apenas analisa quais mensagens não estão presentes em sua conversa e as adiciona. Esta solução minimiza consideralvelmente a chance de perder uma mensagem e garante que toda mensagem trocada no sistema vai eventualmente está presente em todas as conversas. A unica forma de um usuário não possuir uma mensagem é se caso o pacote contendo aquela mensagem em específico falhe no momento em que ela foi enviada e falhe em cada um dos nós durante a sincronização já que pelo menos um pacote com ela precisa chegar, o que faria com que o usuário ficasse sem aquela mensagem por alguns segundos até a proxima sincronização. 

  Por fim, cabe falar a respeito de outro aspecto importante do sistema: a criptografia. Ela pode ser feita de diversas formas e existem várias abordagens comuns como o uso do padrão chave publica/privada, porém, para o sistema em questão foi adotada uma forma de criptografia mais simples. Já que o conteúdo sensível que é passado nos pacotes é o conteúdo das mensagens, uma forma de garantir a privacidade desses dados é fazer com que esse conteúdo apenas tenha sentido para os usuários do grupo, ou seja, mesmo que esses pacotes sejam interceptados as mensagens não façam sentido. Isso pode ser alcançado utilizando uma chave de criptografia, uma senha que é utilizada para criptografar e descriptografar as mensagens e que os usuários combinam previamente. Dessa forma, mesmo que alguém consiga interceptar os pacotes e possua de alguma forma o código para descriptografar, ainda sim será necessário conhecer a chave do grupo. 
  
</p>

# 3. Resultados

<p style="text-align: justify;">
  Esta secção apresenta os resultados da implementação das soluções discutida na secção anterior e quais decisões de código foram realizadas para cumprir com o plano traçado para atender os requisitos do problema.

  - Envio e recebimento das mensagens

  O envio e recebimento das mensagens foi implementado utilizando a biblioteca socket nativa da linguagem python. A função send_message é responsável por enviar uma unica mensagem definida pelo tipo e conteudo a todos os pares ip/porta que compõe o grupo (os membros). Antes de enviar a mensangem, a função gera o objeto do tipo Mensagem que vai guardar aquela mensagem na conversa e o adiciona na lista. No caso do recebimento das mensagens, como apresentado na secção anterior, a função listner fica "escutando" a porta do socket aguardando por novos pacotes e os adicionando em um cachê temporário que é tratado em uma thread paralela com a função pkgSort. 
  
  - Indice e identificador unico

  Para garantir o indice e a forma de identificação unica das mensangens, foram pensadas diversas soluções utilizando geradores de ID, encadeamento de mensagens, entre outros, porém, a adotada foi mais simples e mais eficiente: a utilização de um Relógio Lógico de Lamport. Relógios lógicos são utilizados em sistemas distribuídos para sincronização de mensagens entre sistemas, eles consistem em contadores que se incrementam com suas ações e esse valor do contador é utilizado como um "timestamp" que indica a hora lógica em que aquele evento ocorreu. 
  
  No sistema implementado, já que a ação é cada nó enviar a mensagem para todos os outros nós, o increemento do relógio acontece apenas no envio da mensagem e o reajuste do relógio no recebimento. Os relógios de cada nó não precisam ter o mesmo valor para estarem sincronizados, eles precisam apenas respeitar a seguinte regra: Toda mensagem recebida é um evento do passado, ou seja, foi escrita e enviada em um tempo lógico do passado, dessa forma elas obrigatóriamente devem possuir um tempo lógico menor do que o do relógio lógico do nó que está a recebendo. Caso o timestamp dela seja maior do que a hora lógica do nó, esta mensagem está vindo do futuro (o que é impossivel) então isso significa que o relógio está atrasado e deve ser ajustado para o tempo lógico N + 1, sendo N o timestamp da mensagem. A figura abaixo representa visualmente o processo de troca de mensagens entre dois nós com seus respectivos relógios lógicos.
</p>

![Visualização do relógio logico.](https://github.com/JFooley/PBL-Redes-Problema2-WhatsApp-II/blob/b4f6e379d137003a113947a62d037f8aee8e7b68/Imagens/Imagem%201.png)

<p style="text-align: justify;">
  O nó A envia uma mensagem para o nó B no tempo lógico 10, esta mensagem é recebida no tempo lógico 15 e como 10 é menor que 15, o relógio de B está ajustado corretamente. Já no caso da segunda mensagem, B envia para A uma mensagem com o tempo lógico 25 que é recebida no tempo 23 do nó A, já que 25 > 23 o relógio de A está atrasado e portante deve ser ajustado para o tempo lógico 26 (25 + 1).

  Uma vez que os relógios só aumentam seus valores e cada mensagem incrementa o relógio na hora de enviar (ou seja, ela possui a hora anterior +1), o timestamp da hora lógia das mensagens pode ser utilizado como o indice para odernar as mensagens. Cada nó, ao enviar uma mensagem, passa na frente dos outros que possuam a mesma hora e "puxa" os demais nós para uma hora lógica ajustada acima (caso estejam atrás). 
  
  Um problema dessa abordagem é o caso de duas mensagens serem enviadas ao mesmo tempo e coincidirem o tempo lógico ou de algum nó não recebe alguma mensagem e isso gerar um atraso que possa fazer duas mensagens terem timestamps iguais. Sendo assim, esse timestamp não pode ser utilizado como o identificador unico da mensagem na rede e não garante sozinho a ordem do todo, porém, ele garante a unicidade e a ordem das mensagens do nó que está enviando elas, já que esse contador não pode decrementar e repetir um valor. Para garantir então a unicidade e a ordem na conversa toda basta que as mensagens também guardem uma identificação de quem as enviou. Já que cada nó possui um conjunto ip/porta próprio e unico, utilizando a junção de timestamp + ip/porta conseguimos identificar cada menasagem de forma unica no sistema e utilizar o valor do ip/porta como critério de desempate ao ordernar as mensagens com o timestamp. 

  - Ordenação total
  
  Tendo as mensagens universalmente identificadas e com um atributo que dá ordem a elas (timestamp), a classe dos objetos "Mensagem" (que guardam as informações de cada mensagem) foi modificada para que suas instancias sejam comparadas utilizando o par timestamp + usuário e considere como iguais dois objetos com valores iguais nesses atributos. Essa modificação permite utilizar uma função sort padrão das listas sem a necessidade de implementar um algorítimo de ordenação e garante que todos vão possuir apenas uma cópia de cada mensagem unica e elas serão ordenadas de forma igual para todos os nós.

  - Sincronização

  Visando alcançar o sistema de sincronização proposto, foi implementada uma diferenciação nos pacotes pelo seu tipo, sendo eles: MSG, mensagem comum, enviada naquele momemnto; SYN, pacote de sicronização, que solicita que os demais nós enviem suas conversas; CSP (chat sync part), "pedaço" da conversa enviado como sincronização, ou seja, mensagens antigas individuais.
    
  Para enviar a conversa foi criada uma função sendChat que envia para o nó solicitante cada uma das mensagens antigas como pacotes do tipo CSP, com exceção apenas dos que possuem o mesmo endereço do nó solicitante. Essa função é chamada quando uma mensagem do tipo SYN é retirada da fila do cachê e lida pela thread pkgSort. Já no caso da solicitação de sincronização ela é feita no início do programa, antes de enviar a primeira mensagem, através do envio de um pacote SYN e também eventualmente pela thread eventualSync, que envia um pacote SYN a cada X segundos. O tempo de X é determinado pela constante SYNCTIME. Vale ressaltar que esssa sincronização também faz com que o usuário recupere as mensagens antigas ao entrar em uma conversa em andamento. 

  - Conversa

  Para implementar a conversa, foi decidido que os objetos Mensagem seriam guardados em uma estrutura do tipo Set ao invés de uma lista. Essa decisão foi feita devido as caracteristicas de um Set de não poder possuir mais de uma instancia do mesmo objeto e como a classe Mensagem foi modificada de forma a que duas mensagens sejam considerada iguais a partir de seus atributos, a utilização de um Set para representar a conversa garante essa unicidade das mensagens e facilita no processo de incorporação das mensagens antigas que não estejam presentes na conversa. Entretando, um set é um tipo de estrutura que não possui ordem em seus elementos (diferentemente da lista), então, para poder ordernar essas mensagens, a função printSort gera uma copia da conversa como uma lista e ordena utilizando o metodo Sort no momento em que ela vai ser mostrada na tela. Como a função printSort só é chamada quando há uma mudança na conversa (uma nova mensagem chega ou é enviada), o algorítimo de ordenação não precisa ficar sendo executado de forma desnecessária.

  - Criptografia
    
  Como discutido na secção anterior, a solução pensada para o sistema foi uma chave de criptografia previamente determinada pelos usuários que permite os nós interpretarem o conteúdo das mensagens. No código, a encriptação da mensagem é feita no mommento em que o input da mensagem é inserido e a decriptação apenas no momemnto em que a mensagem vai ser exibida na tela, ou seja, a mensagem permanece encriptada durante todo o funcionamento do programa em que ela não está sendo exibida pro usuário.

  A encriptação e decriptação é feita respectivamente pelas funções encrypt e decrypt. Elas funcionam com um mecanismo básico de embaralhamento de caracteres em que cada letra é transformada em seu valor numérico e depois é somado a um dos digitos da chave a depender do indice da letra que está sendo trocada para, por fim, ser transformada novamente em um novo caractere. A função de decriptação funciona de forma análoga, com a unica diferença de que ao invés de somar o digito é subtraído, o que faz com que volte ao caractere original. 
</p>

# 4. Considerações finais
<p style="text-align: justify;">
  As soluções adotadas descritas neste relatório resultam em um programa relativamente simples mas que cumpre os requisitos apresentados pelo problema de oferece um chat de mensagens instantâneas com arquitetura de sistema distribuído que oferece troca de mensagens consensualmente ordenadas e criptografadas, utilizando o protocolo UDP e considerando o modelo de falhas.

  Apesar de cumprir com seu papel, o programa tem algumas desvantagens conhecidas devido a natureza da sua implementação, sendo elas: inundação da rede com mensagens CSP diretamente proporcional ao crescimento da conversa; criptografia simples e eficiente, porém não ideal para aplicações de maior escala e muito menos para aplicações na internet; dessincronização temporária no limite da perda do pacote da mensagem em todos os nós durante a sincronização; ausencia de confirmação de pacotes através de ACKs.
  
  Dessa forma, algumas melhorias que podem ser futuramente implementadas no código futuramente. Uma delas é o envio da lista dos identificadoes unicos das mensagens para os nós durante a sincronização, pois dessa forma cada nó iria analisar e enviar de volta apenas as mensagens ausentes, sanando o problema de inundação da rede com pacotes CSP. Outro ponto que pode ser aprimorado no sistema é a implementação de um gatilho mais eficiente para a sincronização eventual que não dependa de tempo, principalmente se for um que utilize alguma parametro estatistico (como a taxa de perda de pacotes) para determinar se a conversa pode ou não está comprometida e solicitar a sincronização. Por fim, uma mudança voltada a tornar a aplicação mais "user friendly" é fazer com que cada usuario possua um nome e, através de um broadcast, a aplicação mostre ao usuário o nome dos usuários online, permitindo ele criar o grupo apenas digitando os nomes e abstraindo por trás toda a parte de inserção de ip/porta dos participantes.
</p>

# 5. Referencias
<p style="text-align: justify;">
  threading — Thread-based parallelism. Python Software Foundation. 2023. Disponível em: https://docs.python.org/3/library/threading.html. Acesso em: 22 de novembro de 2023.

  socket — Interface de rede de baixo nível. Python Software Foundation. 2023. Disponível em: https://docs.python.org/pt-br/3/library/socket.html Acesso em: 24 de novembro de 2023.

  pickle — Python object serializatio. Python Software Foundation. 2023. Disponível em: https://docs.python.org/3/library/pickle.html Acesso em: 24 de novembro de 2023.

  CARVALHO, Marcus. Sistemas Distribuídos - 5.2 Relógios lógicos. YouTube, 2023. Disponível em: https://www.youtube.com/watch?v=xK0K3RY5xco&t=1452s Acesso em: 01 de Dezembro de 2023.

</p>

