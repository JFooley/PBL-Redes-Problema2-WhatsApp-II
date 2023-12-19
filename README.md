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
  
  Junto com esse fenomeno uma questão se torna bastante relevante: a proteção dos dados dessas converasas. Sejam conversas pessoais ou decisões importantes de empresas, a privacidade do que é transmitido através dos pacotes pela rede é essencial uma vez que esses dados circulam por diversos dispositivos até chegarem em seus destinos finais e podem ser interceptados por sniffers de rede ou outras tecnologias nos nós. Sendo, assim a criptografia se apresenta como um aspecto importante na implementação desses mensageiros.

  Outro aspecto importante, principalmente no ambito de empresas é a questão da ordenação dessas mensagens. Em uma conversa casual entre pessoas, a ordem que as mensagens chegam é importante já que ela afeta o sentido do que é dito, porém, pequenas divergencias na ordem como de mensagens enviadas "ao mesmo tempo" não são um problema tão relevante. Entretando, quando essas mensageiros estão sendo usados no ambito profissional, a divergencia de ordem nas mensagens podem causar diversos problemas, principalmetne quando elas são utilizadas para sincronizar eventos de duas ou mais partes. Por esse motivo, outro ponto relevante na questão dos chats de mensagens instantâneas é a ordenação total das mensagens nos usuários participantes.

  Pensando nisso, esse relatório descreve o desenvolvimento de um mensageiro simples de troca de mensagens instantâneas em uma rede LAN desenvolvido para o mercado corporativo baseado no modelo peer-to-peer descentralizado que possibilite a comunicação entre usuários de um grupo de forma segura. Além disso, o sistema deve oferecer confiabilidade para  garantir que todos os usuários recebam todas as mensagens na mesma ordem, mesmo aquelas que o usuário não tenha recebido por estar offiline (voluntáriamente ou por desconexão). Além disso, o protótipo deve seguir as seguintes características:
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
  
  A ultima thread que é executada sozinha no programa é a eventualSync, uma thread responsável por executar solicitações de sincronização para os nós da rede para garantir que as mensagens se mantenham atualizadas. Essa solicitação é realizada de X em X tempo, sendo esse X definito em código. Dessa forma, mesmo que um pacote se perca, aquela mensagem não vai ser perdida já que para isso acontecer ela teria que falhar na vinda de todos os computadores da rede. 
  
</p>

# 3. Resultados
<p style="text-align: justify;">
  
</p>

# 4. Considerações finais
<p style="text-align: justify;">
  
</p>

# 5. Referencias
<p style="text-align: justify;">

</p>

