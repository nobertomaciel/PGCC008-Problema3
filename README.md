# PGCC008 - Sistemas Computacionais 2022-1 <br>Atividade #3: Detecção de Emergências (rede mesh)

## Descrição:
<!-- ## Description: -->
Este projeto faz parte da atividade final da disciplina PGCC008 do Programa de Pós-graduação Stricto Sensu em Ciência da Computação (mestrado) da Universidade Estadual de Feira de Santana.
<ul>
   <li>
      <a href="https://github.com/nobertomaciel/PGCC008-Problema3/blob/main/job_description.pdf">job_description.pdf</a>
   </li>
</ul>

<p> Alunos: Noberto Maciel e Gustavo Coelho</p>
<p> Professores: Ângelo Duarte e Thiago de Jesus</p>

## Diagramas do projeto:
<!-- ## Project diagrams: -->
<p>
   <img src="https://github.com/nobertomaciel/PGCC008-Problema3/blob/main/diagrams/PGCC008_Atividade-3_Diagrams-diagrama%20estrutural.drawio.png">
</p>
<p>
   <img width="960px" src="https://github.com/nobertomaciel/PGCC008-Problema3/blob/main/diagrams/PGCC008_Atividade-3_Diagrams-diagrama%20f%C3%ADsico.drawio.png">
</p>


## NodeMCU ESP8266 v3:
### Códigos
<!-- ### Source codes -->
<ul>
    <li>
       <a href="https://github.com/nobertomaciel/PGCC008-Problema3/tree/main/PGCC008%20endDevices">
         Código fonte genérico (para todos os endDevices da rede).
       </a>
   </li>
</ul>


### Configuração
<ol>
    <li>      
      Para desenvolver e carregar o código fonte no nodeMCU ESP8266 foi usado o Visual Studio Code com a extensão <a href="https://platformio.org/">PlatformIO</a>.
   </li>
    <li>      
       Para usar o código na IDE do Arduino, utilize o arquivo <a href="https://github.com/nobertomaciel/PGCC008-Problema3/blob/main/PGCC008%20endDevices/src/main.cpp">main.cpp</a> mudando a extensão para <b>.ino</b> e retirando a biblioteca <b>Arduino.h</b>.
   </li>
   <li>
      Você pode precisar instalar o driver ch340: <a href="https://github.com/nobertomaciel/PGCC008-Problema3/tree/main/drivers">download aqui</a> (linux - testado em debian) ou <a href="https://github.com/nobertomaciel/PGCC008-Problema3/blob/main/drivers/CH341SER_windows.zip">aqui</a> (windows).
   </li>
   <li>
      Tutorial para usar o ESP8266 na PlatformIO Vs Code <a href="https://www.youtube.com/watch?v=0poh_2rBq7E">aqui</a>
   </li>
   <li>
      Tutorial para usar o ESP8266 na IDE Arduino <a href="https://github.com/nobertomaciel/PGCC008-Problema3/blob/main/tutorials/nodeMcu_on_Arduino_IDE.md">aqui</a>
   </li>
   <li>
      Protocolo de comunicação entre sensores e pinagem na <a href="https://github.com/nobertomaciel/PGCC008-Problema3/issues/2">issue #2.</a>
   </li>
</ol>

### Sites
<ol>
   <li>
      <a href="https://www.instructables.com/Add-Custom-Alexa-Control-to-Raspberry-Pi-Project/">https://www.instructables.com/Add-Custom-Alexa-Control-to-Raspberry-Pi-Project/</a>
   </li>
   <li>
      <a href="https://www.raspberrypi.com/software/operating-systems/">https://www.raspberrypi.com/software/operating-systems/</a>
   </li>
   <li>
      <a href="https://docs.aws.amazon.com/pt_br/lambda/latest/dg/welcome.html">https://docs.aws.amazon.com/pt_br/lambda/latest/dg/welcome.html</a>
   </li>

</ol>
