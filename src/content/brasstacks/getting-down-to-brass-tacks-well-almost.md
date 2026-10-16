---
title: "Getting down to Brass Tacks (well almost…)"
pubDate: 2010-10-06
postedAt: "09:06 PM"
description: "OK, I’ve finally decided to take the plunge and start a blog on Storage Area Networks. Why now? Well…thanks to things like FCoE, there’s a lot going on and a ton of new things to learn. I figure as I’m learning and figuring out what makes sense in our lab,..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2010/10/getting-down-to-brass-tacks-well-almost.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250912230543/https://brasstacksblog.typepad.com/brass-tacks/2010/10/getting-down-to-brass-tacks-well-almost.html"
pdf: "/brasstacks/getting-down-to-brass-tacks-well-almost/getting-down-to-brass-tacks-well-almost.pdf"
comments:
  - author: "Suzanne Correia"
    date: "10/06/2010 at 09:28 PM"
    html: |-
      <p>Hey Erik, </p>
      <p>This is very cool and informative.  I especially appreciate your modesty and humor.  Very engaging!  Aside from the technical content, I appreciate your approach to learning: encouraging risk, etc.  Thanks for sharing your insight and knowledge.  Look forward to reading more and keeping informed, especially with regard to your determination to provide good documentation.  I am keen to do what I can to support you in this pursuit. :) </p>
  - author: "Stuart Miniman"
    date: "10/07/2010 at 10:17 AM"
    html: |-
      <p>Welcome to the blogosphere!  </p>
  - author: "Chuck Hollis"
    date: "11/04/2010 at 06:11 PM"
    html: |-
      <p>Erik --</p>
      <p>This is great!  More, please!</p>
      <p>-- Chuck</p>
---

<p class="MsoNormal" style="MARGIN: 0pt"><font size="3"><span style="font-family: Times New Roman;">OK, I’ve finally decided to take the plunge and start a blog on Storage Area Networks.<span style="mso-spacerun: yes">&#0160; </span>Why now?<span style="mso-spacerun: yes">&#0160; </span>Well…thanks to things like FCoE, there’s a lot going on and a ton of new things to learn.<span style="mso-spacerun: yes">&#0160; </span>I figure as I’m learning and figuring out what makes sense in our lab, I’d share some of those experiences and maybe make someone else’s life easier.<span style="mso-spacerun: yes">&#0160; </span></span></font></p>
<p class="MsoNormal" style="MARGIN: 0pt"><o:p><span size="3" style="font-family: Times New Roman;">&#0160;</span></o:p></p>
<p class="MsoNormal" style="MARGIN: 0pt"><font size="3"><span style="font-family: Times New Roman;">To give you a bit of an idea of whom I am, I’ve been working with Fibre Channel in various capacities over the past 11 years for EMC.<span style="mso-spacerun: yes">&#0160; </span>I started with the “Stampede” product line, now known as “Connectrix”, and my first job was to make sure the “dial home” server didn’t hang from all of the McDATA ED-1032 dial homes.<span style="mso-spacerun: yes">&#0160; </span>After that, I spent a brief amount of time in the PSE lab before joining level 2 Tech Support as a member of the ESN (Enterprise Storage Network) team.<span style="mso-spacerun: yes">&#0160; </span>From there it was off to E-Lab and I’ve been there for the past 7 years.<span style="mso-spacerun: yes">&#0160; </span></span></font></p>
<p class="MsoNormal" style="MARGIN: 0pt"><o:p><span size="3" style="font-family: Times New Roman;">&#0160;</span></o:p></p>
<p class="MsoNormal" style="MARGIN: 0pt"><span size="3" style="font-family: Times New Roman;">In E-Lab, as a member of the IOP team, my first set of responsibilities was to qualify new McDATA firmware and hardware.<span style="mso-spacerun: yes">&#0160; </span>Since then I’ve helped to re-write the EMC Networked Storage Topology Guide, co-authored two EMC Tech books (SAN concepts and Protocols and the <a href="https://www.google.com/url?sa=t&amp;source=web&amp;cd=1&amp;sqi=2&amp;ved=0CBUQFjAA&amp;url=http%3A%2F%2Fwww.emc.com%2Fcollateral%2Fhardware%2Ftechnical-documentation%2Fh6290-fibre-channel-over-ethernet-techbook.pdf&amp;ei=6RutTIi_EoO78gaMgO2FDw&amp;usg=AFQjCNEWW768BIPwmgI1gihgTfN8UNwShw">FCoE Tech book</a>), presented at EMC world a handful of times and joined T11 as one of EMC’s Alternates.</span></p>
<p class="MsoNormal" style="MARGIN: 0pt"><o:p><span size="3" style="font-family: Times New Roman;">&#0160;</span></o:p></p>
<p class="MsoNormal" style="MARGIN: 0pt"><font size="3"><span style="font-family: Times New Roman;">Along the way I’ve made probably every mistake you can imagine and all indications are I will continue this tradition going forward!<span style="mso-spacerun: yes">&#0160; </span>Sometimes the root cause for a mistake is a simple case of PEBKAC (problem exists between keyboard and chair) but more frequently I find that documentation is to blame.<span style="mso-spacerun: yes">&#0160; </span>This is one of the reasons why like participating in the creation and re-writing of documentation.<span style="mso-spacerun: yes">&#0160; </span>I know the pain of trying to figure something out using poor documentation.<span style="mso-spacerun: yes">&#0160; </span></span></font></p>
<p class="MsoNormal" style="MARGIN: 0pt"><o:p><span size="3" style="font-family: Times New Roman;">&#0160;</span></o:p></p>
<p class="MsoNormal" style="MARGIN: 0pt"><font size="3"><span style="font-family: Times New Roman;">Over the next few weeks, I’m going to focus on the some of the new improvements we are making to the Networked Storage Topology Guide as well as the Nexus 5000 / Nexus 2232 configuration we just added to the October release.<span style="mso-spacerun: yes">&#0160; </span>After that I’m planning to discuss our experiences with vPC and provide an update to the proposals that we are working on in T11.<span style="mso-spacerun: yes">&#0160; </span>Things a still a bit up in the air but that’s the plan anyway…<span style="mso-spacerun: yes">&#0160; </span></span></font></p>
<p class="MsoNormal" style="MARGIN: 0pt"><o:p><span size="3" style="font-family: Times New Roman;">&#0160;</span></o:p></p>
<p class="MsoNormal" style="MARGIN: 0pt"><span size="3" style="font-family: Times New Roman;">Thanks for reading!</span></p>
<p class="MsoNormal" style="MARGIN: 0pt"><o:p><span size="3" style="font-family: Times New Roman;">&#0160;</span></o:p></p><span style="FONT-FAMILY: &#39;Times New Roman&#39;; FONT-SIZE: 12pt; mso-fareast-font-family: &#39;Times New Roman&#39;; mso-ansi-language: EN-US; mso-fareast-language: EN-US; mso-bidi-language: AR-SA">Erik </span>
