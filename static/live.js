const configNode=document.querySelector('#live-room-config');
const cfg={api:configNode.dataset.api,signals:configNode.dataset.signals,recording:configNode.dataset.recording,csrf:configNode.dataset.csrf,userId:+configNode.dataset.userId,lecturer:configNode.dataset.lecturer==='true'};
const board=document.querySelector('#board'),localVideo=document.querySelector('#local-camera'),remoteVideo=document.querySelector('#remote-camera');
let stream=null,changed=false,airPen=true,lastPen=null,signalCursor=0,recorder=null,chunks=[],recordStarted=0,recordDone=null;
const peers=new Map(),participantIds=new Set(),history=[];
const esc=s=>{const d=document.createElement('div');d.textContent=s;return d.innerHTML};
async function api(url,data,form=false){const o=data?{method:'POST',headers:{'X-CSRFToken':cfg.csrf},body:form?data:JSON.stringify(data)}:{};if(data&&!form)o.headers['Content-Type']='application/json';const r=await fetch(url,o);if(r.status===404){location.href='/dashboard/';return null}const b=await r.json();if(!r.ok)throw new Error(b.error||'Request failed');return b}

let ctx=null;
if(board){ctx=board.getContext('2d');ctx.lineCap='round';ctx.lineJoin='round';
 const saveHistory=()=>{history.push(ctx.getImageData(0,0,board.width,board.height));if(history.length>20)history.shift()};saveHistory();
 const draw=(p,continuing=true)=>{if(!p)return;if(continuing&&lastPen){ctx.beginPath();ctx.moveTo(lastPen.x,lastPen.y);ctx.lineTo(p.x,p.y);ctx.lineWidth=+document.querySelector('#width').value;ctx.strokeStyle=document.querySelector('#color').value;ctx.globalCompositeOperation=document.querySelector('#eraser').dataset.on==='true'?'destination-out':'source-over';ctx.stroke();changed=true}lastPen=p};
 const pos=e=>{const r=board.getBoundingClientRect();return{x:(e.clientX-r.left)*board.width/r.width,y:(e.clientY-r.top)*board.height/r.height}};
 let pointer=false;board.onpointerdown=e=>{pointer=true;saveHistory();lastPen=pos(e)};board.onpointermove=e=>{if(pointer)draw(pos(e))};board.onpointerup=board.onpointerleave=()=>{pointer=false;lastPen=null};
 document.querySelector('#eraser').onclick=e=>{e.currentTarget.dataset.on=e.currentTarget.dataset.on==='true'?'false':'true';e.currentTarget.classList.toggle('active')};
 document.querySelector('#clear').onclick=()=>{saveHistory();ctx.clearRect(0,0,board.width,board.height);changed=true};
 document.querySelector('#undo').onclick=()=>{if(history.length>1){history.pop();ctx.putImageData(history[history.length-1],0,0);changed=true}};
 document.querySelector('#air-pen-toggle').onclick=e=>{airPen=!airPen;e.currentTarget.textContent=airPen?'🖊 Air pen ON':'🖊 Air pen OFF';e.currentTarget.classList.toggle('active',airPen);lastPen=null};
 document.querySelector('#network-diagram').onclick=()=>{saveHistory();ctx.clearRect(0,0,board.width,board.height);ctx.globalCompositeOperation='source-over';ctx.font='bold 30px sans-serif';ctx.textAlign='center';
  const nodes=[['PC',150],['Switch',460],['Router',790],['Server',1130]],y=360;nodes.forEach(([t,x],i)=>{ctx.fillStyle='rgba(255,255,255,.78)';ctx.strokeStyle='#46f0c2';ctx.lineWidth=4;ctx.fillRect(x-80,y-45,160,90);ctx.strokeRect(x-80,y-45,160,90);ctx.fillStyle='#101827';ctx.fillText(t,x,y+10);if(i<nodes.length-1){ctx.beginPath();ctx.moveTo(x+80,y);ctx.lineTo(nodes[i+1][1]-90,y);ctx.stroke()}});changed=true};
 window.drawAirPoint=(p,found)=>{if(!airPen||!found){lastPen=null;return}draw(p,true)};
}

async function startMedia(){if(stream)return stream;try{stream=await navigator.mediaDevices.getUserMedia({video:{width:{ideal:1280},height:{ideal:720},facingMode:'user'},audio:{echoCancellation:true,noiseSuppression:true}});
 if(localVideo)localVideo.srcObject=stream;document.querySelector('#permission-message').textContent='Camera and laptop microphone are active. Hold a green-marked pen in front of the camera.';
 document.querySelector('#camera-toggle').textContent='📷 Camera ON';if(cfg.lecturer){startTracking();for(const id of participantIds)createOffer(id);await startRecording()}return stream}
 catch(e){document.querySelector('#permission-message').textContent=`Camera/microphone blocked: ${e.message}. Click Camera and choose Allow.`;throw e}}
function stopMedia(){stream?.getTracks().forEach(t=>t.stop());stream=null;document.querySelector('#camera-toggle').textContent='📷 Camera OFF'}
if(document.querySelector('#camera-toggle'))document.querySelector('#camera-toggle').onclick=()=>stream?stopMedia():startMedia();

function startTracking(){const work=document.querySelector('#tracking-canvas');if(!work||!localVideo)return;const wctx=work.getContext('2d');let smooth=null;
 const frame=()=>{if(!stream||!airPen){requestAnimationFrame(frame);return}if(localVideo.readyState>=2){wctx.save();wctx.translate(work.width,0);wctx.scale(-1,1);wctx.drawImage(localVideo,0,0,work.width,work.height);wctx.restore();const data=wctx.getImageData(0,0,work.width,work.height).data;let sx=0,sy=0,n=0;
  for(let y=0;y<work.height;y+=3)for(let x=0;x<work.width;x+=3){const i=(y*work.width+x)*4,r=data[i],g=data[i+1],b=data[i+2];if(g>85&&g>r*1.35&&g>b*1.2){sx+=x;sy+=y;n++}}
  if(n>8){let p={x:(sx/n)*board.width/work.width,y:(sy/n)*board.height/work.height};smooth=smooth?{x:smooth.x*.65+p.x*.35,y:smooth.y*.65+p.y*.35}:p;window.drawAirPoint(smooth,true)}else{smooth=null;window.drawAirPoint(null,false)}}requestAnimationFrame(frame)};frame()}

function peer(id){if(peers.has(id))return peers.get(id);const pc=new RTCPeerConnection({iceServers:[{urls:'stun:stun.l.google.com:19302'}]});stream?.getTracks().forEach(t=>pc.addTrack(t,stream));pc.onicecandidate=e=>e.candidate&&sendSignal(id,'ice',e.candidate.toJSON());pc.ontrack=e=>{if(remoteVideo)remoteVideo.srcObject=e.streams[0]};peers.set(id,pc);return pc}
const sendSignal=(target,type,payload)=>api(cfg.signals,{target_user_id:target,signal_type:type,payload});
async function createOffer(id){const pc=peer(id);if(pc.signalingState!=='stable')return;const offer=await pc.createOffer();await pc.setLocalDescription(offer);await sendSignal(id,'offer',offer)}
async function pollSignals(){try{const d=await api(`${cfg.signals}?after=${signalCursor}`);for(const s of d.signals){signalCursor=Math.max(signalCursor,s.id);const pc=peer(s.sender_id);if(s.type==='offer'){await pc.setRemoteDescription(s.payload);const answer=await pc.createAnswer();await pc.setLocalDescription(answer);await sendSignal(s.sender_id,'answer',answer)}else if(s.type==='answer')await pc.setRemoteDescription(s.payload);else if(s.type==='ice')await pc.addIceCandidate(s.payload)}}catch(e){console.warn(e.message)}}

function setupSpeech(){const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){document.querySelector('#transcript').textContent='Speech text needs Edge or Chrome.';return null}const r=new SR();r.continuous=true;r.interimResults=true;r.lang=navigator.language||'en-US';r.onresult=e=>{let final='',interim='';for(let i=e.resultIndex;i<e.results.length;i++)e.results[i].isFinal?final+=e.results[i][0].transcript:interim+=e.results[i][0].transcript;document.querySelector('#live-caption').textContent=interim||final;if(final){const box=document.querySelector('#transcript');box.textContent=(box.textContent==='Waiting for speech…'?'':box.textContent+'\n')+final;api(cfg.api,{action:'transcript',text:final}).catch(()=>{})}};return r}
let speech=null,speechOn=false;if(document.querySelector('#speech-toggle'))document.querySelector('#speech-toggle').onclick=()=>{if(!speech)speech=setupSpeech();if(!speech)return;speechOn=!speechOn;if(speechOn){speech.start();document.querySelector('#speech-toggle').textContent='⏹ Stop speech'}else{speech.stop();document.querySelector('#speech-toggle').textContent='🎙 Speech text'}};

async function startRecording(){if(!cfg.lecturer||recorder?.state==='recording')return;const composite=document.createElement('canvas');composite.width=1280;composite.height=720;const c=composite.getContext('2d');
 const paint=()=>{if(recorder?.state!=='recording'&&recorder)return;c.save();c.translate(composite.width,0);c.scale(-1,1);if(localVideo.readyState>=2)c.drawImage(localVideo,0,0,composite.width,composite.height);c.restore();if(board)c.drawImage(board,0,0,composite.width,composite.height);requestAnimationFrame(paint)};
 const output=composite.captureStream(30);stream.getAudioTracks().forEach(t=>output.addTrack(t));chunks=[];recorder=new MediaRecorder(output,{mimeType:MediaRecorder.isTypeSupported('video/webm;codecs=vp8,opus')?'video/webm;codecs=vp8,opus':'video/webm'});recorder.ondataavailable=e=>e.data.size&&chunks.push(e.data);recordDone=new Promise(resolve=>recorder.onstop=()=>uploadRecording().finally(resolve));recordStarted=Date.now();recorder.start(1000);paint();document.querySelector('#record-toggle').textContent='🔴 Recording automatically'}
async function uploadRecording(){const blob=new Blob(chunks,{type:'video/webm'}),form=new FormData();form.append('recording',blob,`live-${Date.now()}.webm`);form.append('duration',Math.round((Date.now()-recordStarted)/1000));document.querySelector('#record-toggle').textContent='Saving video…';await api(cfg.recording,form,true);document.querySelector('#record-toggle').textContent='✓ Video saved'}
async function stopRecording(){if(recorder?.state==='recording'){recorder.stop();await recordDone}}
document.querySelector('#record-toggle')?.addEventListener('click',async()=>recorder?.state==='recording'?stopRecording():startRecording());

async function refresh(){try{if(cfg.lecturer&&changed){await api(cfg.api,{action:'board',image:board.toDataURL('image/png')});changed=false}const d=await api(cfg.api);if(!d)return;if(!cfg.lecturer&&d.board)document.querySelector('#live-board').src=d.board;document.querySelector('#count').textContent=`(${d.participants.length+1})`;document.querySelector('#participants').innerHTML=`<p>👨‍🏫 ${esc(d.lecturer)}</p>`+d.participants.map(p=>`<p>${p.hand?'✋':'👨‍🎓'} ${esc(p.name)}</p>`).join('');document.querySelector('#messages').innerHTML=d.messages.map(m=>`<p><b>${esc(m.name)}</b> ${esc(m.text)}</p>`).join('');if(cfg.lecturer)for(const p of d.participants)if(!participantIds.has(p.id)){participantIds.add(p.id);if(stream)createOffer(p.id)}}catch(e){console.warn(e.message)}}
document.querySelector('#send-chat').onclick=async()=>{const i=document.querySelector('#chat-text');if(i.value.trim())await api(cfg.api,{action:'chat',text:i.value});i.value='';refresh()};
document.querySelector('#raise-hand')?.addEventListener('click',()=>api(cfg.api,{action:'hand'}).then(refresh));
document.querySelector('#end-live')?.addEventListener('click',async()=>{document.querySelector('#end-live').disabled=true;await stopRecording();await api(cfg.api,{action:'end'});location.href='/dashboard/'});
refresh();pollSignals();setInterval(refresh,1400);setInterval(pollSignals,900);if(cfg.lecturer)startMedia();
