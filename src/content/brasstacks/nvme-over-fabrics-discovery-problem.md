---
title: "NVMe over Fabrics’ Discovery problem"
pubDate: 2017-12-07
postedAt: "10:56 AM"
description: "TL;DR – Today, Fibre Channel provides an NVMe over Fabrics Discovery mechanism, Ethernet does not. This blog post describes an investigation that was performed to determine if an enhancement to the NVMe over Fabrics Discovery protocol was needed in order for it to support a Network Centric connectivity model as..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2017/12/nvme-over-fabrics-discovery-problem.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250913100238/https://brasstacksblog.typepad.com/brass-tacks/2017/12/nvme-over-fabrics-discovery-problem.html"
pdf: "/brasstacks/nvme-over-fabrics-discovery-problem/nvme-over-fabrics-discovery-problem.pdf"
comments: []
---

<p>TL;DR – Today, Fibre Channel provides an <a class="zem_slink" href="https://en.wikipedia.org/wiki/NVM_Express" rel="wikipedia noopener noreferrer" target="_blank" title="NVM Express">NVMe</a> over Fabrics Discovery mechanism, Ethernet does not. &#0160;</p>
<p>This blog post describes an investigation that was performed to determine if an enhancement to the NVMe over Fabrics Discovery protocol was needed in order for it to support a Network Centric connectivity model as described below.&#0160; The investigation determined that a multi-layer discovery technique was called for and that FC already provided the required Discovery mechanisms; Ethernet currently does not.</p>
<p>Before I continue I need to thank Dave Peterson (Broadcom) for his assistance with the FC Discovery portion of this investigation.&#0160; &#0160;</p>
<h2>Management models</h2>
<p>In order for NVMe over Fabrics (NVMe-oF) to be widely adopted, I believe it must integrate into existing workflows and management tools (e.g., provisioning and monitoring) that existing enterprises use when managing external (e.g., Array based) storage.&#0160; As of today, there are three primary approaches that can be utilized for this purpose:</p>
<ol>
<li><strong>A Centralized <a class="zem_slink" href="http://www.wikinvest.com/concept/Cloud_Computing" rel="wikinvest noopener noreferrer" target="_blank" title="Cloud Computing">Infrastructure as a Service (IaaS)</a> Management and Orchestration (M&amp;O) layer</strong>. OpenStack is one example of an open source project that provides this functionality, but some users are opting to write their own custom M&amp;O Layer by making use of workflow orchestration frameworks (e.g., Stackstorm), while leveraging tools (e.g., Ansible) and/or extensions to languages (e.g., Pyvmomi).&#0160; This type of approach is typically used by larger customers with extensive development resources.&#0160; This type of approach can be used with both the “End-node Centric” and “Network Centric” provisioning models described below.&#0160; I should also point out that <a href="/brasstacks/the-iaas-missing-link/">the IaaS Missing Link</a> is something that complicates this kind of approach.&#0160; &#0160;</li>
<li><strong>The “End-node Centric” management model</strong>. This approach requires every host and storage resource to be individually configured and is primarily used in Small and Medium Business (SMB) environments to manage access to storage when NFS/CIFS or iSCSI are being used.&#0160; The benefit to this approach is “simplicity” and the fact that a centralized discovery service does not need to be installed nor configured.&#0160; The downside to this model is that it doesn’t scale very well; as the number of nodes increases the administrative burden increases non-linearly.</li>
<li><strong>The “Network Centric” management model</strong>. This approach utilizes a centralized Discovery Service to enable Hosts to discover the Storage ports that are available to it.&#0160; This type of approach is used in Medium and Large Enterprise environments to manage connectivity in their Fibre Channel (FC) <a class="zem_slink" href="https://en.wikipedia.org/wiki/Storage_area_network" rel="wikipedia noopener noreferrer" target="_blank" title="Storage area network">Storage Area Networks</a> (SANs).&#0160; The benefit to this approach is that it scales fairly well (10k+ ports with FC today) and supports State Change Notifications.&#0160; The downside is a centralized service must be installed and in some cases configured.&#0160; Another limitation is the requirement that all host and storage subsystem ports register with the centralized Discovery Service.</li>
</ol>
<p>For more information about the “Network Centric” and End-node Centric” management models as well as the scalability attributes of each, please refer to <a href="/brasstacks/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning/">FC and FCoE versus iSCSI – “Network-centric” versus “End-Node-centric” provisioning</a></p>
<p>Since NVMe over Fabrics will need to scale (e.g., beyond a single rack) I believe it makes sense for the Transports to at least support a “Network Centric” management model.</p>
<p>In addition, since NVMe over Fabrics will need to co-exist with SCSI and SCSI-FCP, it makes sense to follow a layered discovery approach that is similar to what has been done for discovery with those protocols.&#0160;&#0160;&#0160;</p>
<h2>The Network Centric management model</h2>
<p>In order to support the “Network Centric” management model, this blog post breaks discovery into two different layers; NVMe and Transport Specific.&#0160; This separation will allow for the existing NVMe Discovery process to remain intact while allowing each Transport to leverage existing transport specific approaches for the discovery of Transport Addresses that support a specific feature (i.e., a Discovery Service).&#0160; This concept is illustrated in the diagram below.&#0160;</p>
<p><a class="asset-img-link" href="/brasstacks/nvme-over-fabrics-discovery-problem/6a013487ed263f970c01bb09de0992970d.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01bb09de0992970d image-full img-responsive" src="/brasstacks/nvme-over-fabrics-discovery-problem/6a013487ed263f970c01bb09de0992970d.jpg" title="One" /></a></p>
<p>The Network Centric approach and how the layered approach will impact each transport is described below.</p>
<p><strong><u>Transport Specific Discovery</u></strong></p>
<p>In order to automate the discovery of end devices (e.g., Arrays) that support NVMe over Fabrics, I believe a “centralized”, Transport Specific, Discovery Service is needed.&#0160; Furthermore, this Discovery Service will need to be able to provide a list of Transport Specific addresses that provide an NMVe Discovery Controller (e.g., that reside on each NVMe Subsystem).</p>
<p>Side note: Transport Specific Discovery is totally optional.&#0160; Outside of expected behavior, the implementation details regarding a particular Transport Specific Discovery Service will probably not be defined in the NVMe over Fabrics specification.</p>
<p>Although this may seem obvious to some of you, it’s important to explicitly state that each of the protocols would need to handle Transport Specific Discovery in a Transport independent way, for example:</p>
<h3>Fibre Channel</h3>
<p>The Transport Specific Discovery Service for FC is the Name Server and is defined in the Fibre Channel standard FC-GS.&#0160; The Discovery Service capability is returned to the Host port in response to “Get N_Port Identifier for the specified FC-4 Feature” (GID_FF) with the FC-4 feature of 28h specified and the FC-4 Discovery Service Feature bit set to 1.&#0160; When the FC Transport Discovery process is complete, the Host port will have a list of all FC WWPNs and N_Port IDs that provide an NVMe Discovery Controller.&#0160; This requires that each VN_Port properly register its FC-4 features.</p>
<h3>IP</h3>
<p>Transport Specific Discovery for IP could be provided in a number of ways, including:</p>
<ul>
<li>manual configuration,</li>
<li>via a configuration management tool (e.g., Ansible, Puppet), or</li>
<li>a centralized service (as described below) could be deployed and then discovered via DHCP:</li>
</ul>
<ol>
<li>The location of the Transport Discovery Service for IP (e.g., <a class="zem_slink" href="https://en.wikipedia.org/wiki/Internet_Storage_Name_Service" rel="wikipedia noopener noreferrer" target="_blank" title="Internet Storage Name Service">iSNS</a> could be enhanced and used) can be discovered via DHCP.</li>
<li>The Hosts and Discovery Controllers will need to register their NQN, Transport Address and Discovery Service capability with the Transport Discovery Service. These registration commands still need to be defined.</li>
<li>The Hosts and Discovery Controllers will optionally be allowed to register a Discovery Domain (Similar to what is defined for iSNS) with the Transport Discovery Service. The purpose of the Discovery Domain is to limit the number of Discovery Services that each host can access and this serves two purposes:
<ol>
<li>It helps avoid scalability issues related to “Discovery and RSCN Storms”</li>
<li>It provides a coarse grained access control mechanism similar to the role that zoning plays in a FC SAN.</li>
</ol>
</li>
<li>The Hosts and Discovery Controllers will be allowed to query the Transport Discovery Service to determine the transport addresses that are available and of those which of them support a Discovery Service. The commands used to query the Transport Discovery Service will also need to be defined.&#0160;</li>
</ol>
<h3>IB</h3>
<p>For IB I’m going to let Mellanox figure this one out.&#0160; :-)</p>
<h2>NVMe Registration and Discovery</h2>
<p>After the Transport Specific Discovery process has completed, the Host Software can use the Fabric Connect command and specify the well-known Discovery Service NQN as the destination.&#0160; For each Transport Specific address that registered as a Discovery Service and was discovered via the Transport Specific Discovery service, the host software will obtain a Discovery Log page as defined in section 5 of the NVMe over Fabrics 1.0 specification.</p>
<p>As shown in the diagram above, this Discovery Service can either be physically located in the same enclosure as the Controller used for IO (e.g., within the same Array enclosure) or it could be centrally located and accessible over an out-of-band network connection (e.g., to support a rack of JBOF).&#0160; In order to support both of these cases, the information that is registered with the NVMe Discovery Service must allow for a Discovery Log page to be fully populated.&#0160; Since this is the case, the Register Discovery Log Page command should contain one or more Discovery log pages.&#0160;</p>
<p>The Register Discovery Log Page command can be used to directly register a log page but other methods not defined in the NVMe over Fabrics specification may also be used (i.e., when the Discovery Service is located within a storage array).</p>
<p>The format of the Register Discovery Log Page command is also TBD.&#0160;&#0160;&#0160;&#0160;&#0160;</p>
<p><strong><u>State Change Notification</u></strong></p>
<p>With FC, State Change Notification has proven to be amazingly important for operational concerns.&#0160; Essentially, you need to know when a device goes away ASAP and RSCN allows for this.&#0160;</p>
<p>Similar to the approach used with Discovery, the mechanisms used to provide State Change Notification should also be layered into Transport specific and NVMe specific.</p>
<p><strong>Transport Specific</strong></p>
<p>Each Transport may support a mechanism to indicate that a change has occurred in the transport that may affect connectivity.</p>
<p><strong>Fibre Channel – </strong>Fibre Channel provides Asynchronous state change notification via Registered State Change Notification (RSCN)</p>
<p><strong>IP</strong> – I am honestly not sure what could be done here short of adding this functionality to an iSNS like centralized controller.&#0160;</p>
<p><strong>IB</strong> – Again, I’ll defer to Mellanox.</p>
<p><strong>NVMe Specific</strong></p>
<p>State change notification can also be provided between NVMe host software and each controller through the use of the following approaches:</p>
<ul>
<li>Asynchronous Notification for optional events as defined in NVMe over Fabrics 1.0.</li>
<li>Keepalive based monitoring between the NVMe host software and each controller.</li>
<li>A combination of keepalive based monitoring between the NVMe host software/Controller/Discovery Controller and the Transport Discovery Service; with the Transport Discovery Service transmitting an asynchronous event when a keepalive timeout occurs</li>
</ul>
<p>All three of these approaches will need to be defined.</p>
<h2>Conclusion</h2>
<p>As <a href="https://www.youtube.com/watch?v=vH7_AVdWfPc">we’ve said before</a>, NVMe over Fabrics needs a bit more work before it will be ready for use by the majority of our Enterprise Customers.&#0160; Along these lines, I believe that Discovery and State Change Notification are features that will be critically important to you as you start to evaluate different Transports.&#0160;</p>
<p>Thanks for reading! &#0160;</p>
