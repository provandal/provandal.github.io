---
title: "Should I use optical fiber or twinax cable?"
pubDate: 2010-12-22
postedAt: "04:54 PM"
description: "Earlier this week I received a question regarding EMC’s recommendations for using twinax cable. My response is included below, but I need to tip my hat to Mark Lippitt for reviewing, correcting, and adding a couple of different considerations that I overlooked. One other point worth mentioning is that we..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2010/12/should-i-use-optical-fiber-or-twinax-cable.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250912201523/https://brasstacksblog.typepad.com/brass-tacks/2010/12/should-i-use-optical-fiber-or-twinax-cable.html"
pdf: "/brasstacks/should-i-use-optical-fiber-or-twinax-cable/should-i-use-optical-fiber-or-twinax-cable.pdf"
comments:
  - author: "Andrew Fidel"
    date: "12/29/2010 at 04:47 PM"
    html: |-
      <p>This needs to be fixed. The only thing you should need is a standards compliant sfp+ cable. Even in the IT industry this coding to only using special marked up cables is an aboration.</p>
  - author: "Danny DeMichele Entrepreneur"
    date: "03/02/2011 at 06:39 AM"
    html: |-
      <p>I think the above suggestion is good. And I think I will also prefer this. Thanks for sharing such useful information with me. </p>
  - author: "Erik Smith"
    date: "03/02/2011 at 07:20 AM"
    html: |-
      <p>Thanks Danny.  I&#39;m Glad you find the information useful!</p>
      <p>Erik   </p>
  - author: "Jim Nickel"
    date: "03/29/2011 at 05:16 PM"
    html: |-
      <p>Would be super-cool if you would list the EMC part #&#39;s for the 1, 3, and 5m active Twinax cables.</p>
      <p>Jim</p>
  - author: "Erik Smith"
    date: "04/01/2011 at 08:16 PM"
    html: |-
      <p>Hi Jim, good idea, thanks for the suggestion.  I&#39;ll post the model numbers shortly.</p>
  - author: "Paolo"
    date: "06/15/2011 at 05:48 AM"
    html: |-
      <p>Hi Erik,<br />
      Could I connect a “SFP+ 10Gb Twinax Cable” between two servers, without a “ToR switch”?<br />
      Is SFP+ Twinax also a “Crossover Cable”?</p>
      <p>The Configuration for example could be:<br />
      two UCS C-Series Rack-Mount with Qlogic QLE 8152-CNA 2port 10Gb SFP+ Copper</p>
      <p>Thanks much!</p>
      <p>Paolo</p>
  - author: "Erik Smith"
    date: "06/16/2011 at 10:27 AM"
    html: |-
      <p>Hi Paolo, although I&#39;ve never actually tried it, I believe you can connect an SFP+ twinax cable directly between two servers without using a switch.  The cables terminate into SFP+ modules that are standardized to all use a common connector pinout.  As a result, they are all effectively &quot;crossover&quot; cables.  </p>
      <p>Keep in mind that currently FCoE will not function properly in this configuration.     </p>
  - author: "Allen Smith"
    date: "09/16/2011 at 10:51 PM"
    html: |-
      <p>Very resourceful insight! I am currently using optical fiber, now I have seen the big advantages and disadvatages. Thanks for posting this relevant article.</p>
  - author: "Erik Smith"
    date: "09/30/2011 at 07:17 PM"
    html: |-
      <p>Thanks Allen!</p>
  - author: "Peter Thomas"
    date: "01/17/2013 at 08:01 AM"
    html: |-
      <p>@ Jim : EMC TwinAx cables</p>
      <p></p>
      <p>Length<br />
      </p>
      <p>VNX5300<br />
      </p>
      <p>VNX5500/5700/7500<br />
      </p>
      <p>Part #<br />
      </p>
      <p></p>
      <p>1 meter<br />
      </p>
      <p>SFPTWNACT-1MS<br />
      </p>
      <p>SFPTWNACT-1M<br />
      </p>
      <p>038-004-176<br />
      </p>
      <p></p>
      <p>3 meter<br />
      </p>
      <p>SFPTWNACT-3MS<br />
      </p>
      <p>SFPTWNACT-3M<br />
      </p>
      <p>038-004-177<br />
      </p>
      <p></p>
      <p>5 meter<br />
      </p>
      <p>SFPTWNACT-5MS<br />
      </p>
      <p>SFPTWNACT-5M<br />
      </p>
      <p>038-004-178<br />
      <br />
      </p>
  - author: "Erik"
    date: "01/17/2013 at 08:29 AM"
    html: |-
      <p>Thanks Peter!</p>
---

<p>Earlier this week I received a question regarding EMC’s recommendations for using <a href="https://en.wikipedia.org/wiki/Twinaxial_cabling" target="_self">twinax cable</a>.&#0160; My response is included below, but I need to tip my hat to Mark Lippitt for reviewing, correcting, and adding a couple of different considerations that I overlooked.&#0160; One other point worth mentioning is that we are working on an update for the February edition of the <a href="http://www.emc.com/collateral/hardware/technical-documentation/h6290-fibre-channel-over-ethernet-techbook.pdf" target="_self">EMC FCoE TechBook</a> that will also include the following information.</p>
<p><strong>Question:</strong> “Should I use optical or twinax connections when connecting my CNAs to the ToR switch?”</p>
<p><strong>Answer: </strong>You can use optical connections for any FCoE link.&#0160; The downside is that they are more expensive and use more power.&#0160; The upside is that you don&#39;t have to worry about distance (up to 300 meters) and, perhaps more importantly, you don&#39;t have to worry about which vendor’s cable you use…<strong></strong></p>
<p>Typically, we see twinax (copper) being used between the server and the Top of Rack (ToR) switch.&#0160; The upside in this configuration is that the twinax connection is much cheaper than the cost of an optical link.&#0160; The downside is that you are limited in distance and there‘s also some cable interoperability issues you’ll need to deal with.</p>
<p>In regards to active versus passive twinax cables, it depends on what you are connecting together:</p>
<p><em>Note: The following information assumes that either FOS 6.4.1 (or later) or NX-OS 4.2(1)N2(1) (or later) is being used.</em></p>
<ul>
<li>If you are connecting a CNA to a Cisco ToR switch (Nexus) and the cable length is 1, 3, or 5m, you can use a Cisco-supplied 1, 3, or 5m passive twinax cable or a EMC active twinax 1, 3, or 5m cable. </li>
<li>If you are connecting a CNA to a Cisco ToR switch (Nexus) and the cable length is 7 or 10m, you need to use a Cisco-supplied 7 or 10m active twinax cable.</li>
<li>If you are connecting a CNA to a Brocade ToR switch (8000) and the cable length is 1, 3, or 5m, you can use a Brocade-supplied 1, 3, or 5m active twinax cable or an EMC-supplied 1, 3, or 5m active twinax cable.</li>
</ul>
<p>The above assumes that you are using a CNA that supports a given flavor of twinax.&#0160; As of right now, the QLogic 815x and Emulex OCe1012, support either active or passive twinax from both Cisco and QLogic.&#0160; The Brocade CNAs support active twinax from Brocade or EMC’s active twinax cable.&#0160;</p>
<p>If you want to connect a Brocade CNA to a Cisco ToR switch (Nexus), you could use the EMC active twinax cable.&#0160; Otherwise, you&#39;ll need to use optical since the Cisco switch will log an error if you attempt to use the Brocade cable.<em></em></p>
<p>If you want to attach EMC native FCoE storage (CLARiiON) to a Brocade switch using twinax you can use either:</p>
<ul>
<li>EMC&#39;s 1, 3, or 5m active twinax cable; or</li>
<li>Brocade’s 1, 3, or 5m active twinax.</li>
</ul>
<p>If you want to attach EMC native FCoE storage (CLARiiON) to a Cisco switch using twinax:</p>
<ul>
<li>You can use EMC&#39;s 1, 3, or 5m active twinax cable.</li>
<li>You CANNOT use Cisco’s passive 1, 3, or 5m passive twinax.</li>
<li>We are testing Cisco’s 7, 10m active twinax with native FCoE storage, but this is not completed yet.</li>
</ul>
<p>With regard to compatibility algorithms:</p>
<ul>
<li>Cisco will always bring up a cable if it can. If it does not recognize the cable, it will post an error message to the system log, but bring up the cable.</li>
<li>Brocade and EMC must recognize the cable. If they do not recognize the cable, they will not bring up the link.</li>
</ul>
