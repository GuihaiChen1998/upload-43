// Paper version of render_figures.cjs (main session, round 32): same data and design; in-figure titles
// removed (captions carry them) and text collisions fixed. Writes to paper/figures/gpt/.
const fs=require("node:fs"), path=require("node:path");
function toolkit(){
 const ink="#182734",muted="#4B6172";
 const q=s=>String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;");
 function scene(name,w,h){
  const p=[];
  return {name,w,h,p,
   box(x,y,w,h,fill="#fff",stroke="#c9d4de",r=12,sw=1,dash=false,id){p.push({t:"box",x,y,w,h,fill,stroke,r,sw,dash,id});},
   text(x,y,s,n=17,c=ink,b=false,a="start"){p.push({t:"text",x,y,s,n,c,b,a});},
   edge(points,c=ink,sw=1.7,dash=false,end=false,from,to){p.push({t:"edge",points,c,sw,dash,end,from,to});},
   shape(x,y,r,c,k="circle",stroke="none",sw=1,id){p.push({t:"shape",x,y,r,c,k,stroke,sw,id});},
  };
 }
 function svg(sc){
   const markers=new Set(sc.p.filter(a=>a.t==="edge"&&a.end).map(a=>a.c));
   let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${sc.w}" height="${sc.h}" viewBox="0 0 ${sc.w} ${sc.h}" role="img" aria-label="${q(sc.name)}">\n<title>${q(sc.name)}</title>\n<rect width="100%" height="100%" fill="white"/>\n<defs>`;
   for(const c of markers)s+=`<marker id="arr${c.slice(1)}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="${c}"/></marker>`;
   s+="</defs>\n";
   for(const a of sc.p){
    if(a.t==="box")s+=`<rect x="${a.x}" y="${a.y}" width="${a.w}" height="${a.h}" rx="${a.r}" fill="${a.fill}" stroke="${a.stroke}" stroke-width="${a.sw}"${a.dash?' stroke-dasharray="6 4"':""}/>`;
    if(a.t==="text")s+=`<text x="${a.x}" y="${a.y}" font-family="Arial, Helvetica, sans-serif" font-size="${a.n}" fill="${a.c}" text-anchor="${a.a}" font-weight="${a.b?"700":"400"}" dominant-baseline="central">${q(a.s)}</text>`;
    if(a.t==="edge")s+=`<polyline points="${a.points.map(v=>v.join(",")).join(" ")}" fill="none" stroke="${a.c}" stroke-width="${a.sw}" stroke-linejoin="round" stroke-linecap="round"${a.dash?' stroke-dasharray="5 5"':""}${a.end?` marker-end="url(#arr${a.c.slice(1)})"`:""}/>`;
    if(a.t==="shape"){
      const {x,y,r,c,stroke,sw,k}=a;
      if(k==="circle")s+=`<circle cx="${x}" cy="${y}" r="${r}" fill="${c}" stroke="${stroke}" stroke-width="${sw}"/>`;
      else {const pt=k==="square"?[[x-r,y-r],[x+r,y-r],[x+r,y+r],[x-r,y+r]]:k==="triangle"?[[x,y-r],[x+r,y+r],[x-r,y+r]]:[[x,y-r],[x+r,y],[x,y+r],[x-r,y]];s+=`<polygon points="${pt.map(p=>p.join(",")).join(" ")}" fill="${c}" stroke="${stroke}" stroke-width="${sw}"/>`;}
    }
    s+="\n";
   }
   return s+"</svg>\n";
 }
 function drawio(scenes){
   let s=`<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net" type="device" compressed="false">\n`;
   for(const [j,sc] of scenes.entries()){
     s+=`<diagram id="page-${j+1}" name="${q(sc.name)}"><mxGraphModel grid="0" page="1" pageScale="1" pageWidth="${sc.w}" pageHeight="${sc.h}" background="#ffffff"><root><mxCell id="0"/><mxCell id="1" parent="0"/>\n`;
     const geom=(x,y,w,h)=>`<mxGeometry x="${x}" y="${y}" width="${w}" height="${h}" as="geometry"/>`;
     const vertex=(id,value,style,g)=>`<mxCell id="${id}" value="${q(value)}" style="${style}" vertex="1" parent="1">${g}</mxCell>\n`;
     for(const [i,a] of sc.p.entries()){
       const id=a.id||`i${i+2}`;
       if(a.t==="box")s+=vertex(id,"",`${a.r?"rounded=1;arcSize=12;":"rounded=0;"}html=0;fillColor=${a.fill};strokeColor=${a.stroke};strokeWidth=${a.sw};${a.dash?"dashed=1;":""}`,geom(a.x,a.y,a.w,a.h));
       if(a.t==="text"){
          const w=Math.max(28,Math.ceil(a.s.length*a.n*.61+4));const x=a.a==="middle"?a.x-w/2:a.a==="end"?a.x-w:a.x;
          s+=vertex(id,a.s,`text;html=0;align=${a.a==="middle"?"center":a.a==="end"?"right":"left"};verticalAlign=middle;resizable=1;whiteSpace=wrap;spacing=0;fontFamily=Arial;fontSize=${a.n};fontColor=${a.c};fontStyle=${a.b?1:0};`,geom(x,a.y-a.n*.65,w,a.n*1.3));
       }
       if(a.t==="shape")s+=vertex(id,"",`${({circle:"ellipse;",diamond:"rhombus;",square:"rounded=0;",triangle:"triangle;direction=north;"})[a.k]}html=0;fillColor=${a.c};strokeColor=${a.stroke};strokeWidth=${a.sw};`,geom(a.x-a.r,a.y-a.r,a.r*2,a.r*2));
       if(a.t==="edge"){
         const [x,y]=a.points[0],[xx,yy]=a.points.at(-1);
         const d=a.points.slice(1,-1).map(([x,y])=>`<mxPoint x="${x}" y="${y}"/>`).join("");
         s+=`<mxCell id="${id}" edge="1" parent="1"${a.from?` source="${a.from}"`:""}${a.to?` target="${a.to}"`:""} style="edgeStyle=none;rounded=0;endArrow=${a.end?"block":"none"};endFill=1;endSize=6;strokeColor=${a.c};strokeWidth=${a.sw};${a.dash?"dashed=1;":""}"><mxGeometry relative="1" as="geometry"><mxPoint x="${x}" y="${y}" as="sourcePoint"/><mxPoint x="${xx}" y="${yy}" as="targetPoint"/>${d?`<Array as="points">${d}</Array>`:""}</mxGeometry></mxCell>\n`;
       }
     }
     s+=`</root></mxGraphModel></diagram>\n`;
   }
   return s+"</mxfile>\n";
 }
 return {ink,muted,scene,svg,drawio};
}
function overview(theme,K){
 const titles={editorial:"Illustrated Modular",airy:"Pastel Airy",dual:"Dual-Fidelity Loop"};
 const s=K.scene(titles[theme],1200,586),ink=K.ink,m=K.muted;
 const C={
 editorial:{F:["#e8f2ff","#ecf5e9","#fff0e5"],S:["#4b6e9e","#557658","#a3603c"],bw:2,corner:19,route:"#f4eef8",dark:"#213b50"},
 airy:{F:["#f7faff","#f6fbf8","#fffaf5"],S:["#84a6d7","#8ebbad","#d8a683"],bw:1,corner:18,route:"#f8fafc",dark:"#334155"},
 dual:{F:["#eff6ff","#e6f2ff","#fff0ec"],S:["#6290c6","#4074a6","#c95c4c"],bw:1.4,corner:10,route:"#edf3fa",dark:"#1f344b"}
 }[theme];
 const line=(p,end=true,dash=false,col=m,w=1.65,from,to)=>s.edge(p,col,w,dash,end,from,to);
 const title=(x,y,v)=>s.text(x,y,v,17,ink,true);
 const small=(x,y,v)=>s.text(x,y,v,14,m);
 
 
 const stage=[["Estimator family",228],["Prompt / context",410],["Query draws",571],["Score per source",724]];
 stage.forEach(([l,x])=>s.text(x,89,l,14,m,true));
 const rows=[
  {y:105,n:"A",name:"Self-report",methods:"V1–V7",cells:[["Ask for source IDs","Vanilla · probe · CoT"],["Full context","One or multiple draws"],["Vote over cited IDs","Direct or weighted"]]},
  {y:207,n:"B",name:"Single-source",methods:"P1/P2/P5 · LOI",cells:[["Edit one source","LOO: remove · LOI: keep"],["Query each edit","One or multiple draws"],["Compare with a₀","Answer change / match"]]},
  {y:309,n:"C",name:"Random subsets",methods:"RM@k",cells:[["Draw k keep masks","Bernoulli(½) per source"],["Query each mask","Reuse repeated masks"],["Banzhaf contrast","Mean with vs. without"]]}
 ];
 const x0=205,x1=905;
 line([[169,258],[188,258],[188,151],[x0,151]],true,false,m,1.7,undefined,"laneA");
 line([[188,253],[x0,253]],true,false,m,1.7,undefined,"laneB");
 line([[188,258],[188,355],[x0,355]],true,false,m,1.7,undefined,"laneC");
 line([[x1,151],[926,151],[926,249],[953,249]],true,false,m,1.7,"laneA","rank");
 line([[x1,253],[926,253]],false,false,m);
 line([[x1,355],[926,355],[926,253]],false,false,m);
 s.box(20,192,150,132,theme==="airy"?"#f9fafc":"#f4f7f8","#aabdc9",C.corner,C.bw,false,"input");
 s.text(95,217,"Instance",17,ink,true,"middle");
 s.text(95,247,"Query q",16,ink,false,"middle");
 for(let i=0;i<4;i++)s.box(40+i*27,263,24,19,"#ffffff","#9badbd",4);
 for(let i=0;i<4;i++)s.text(52+i*27,273,["1","2","…","M"][i],13,ink,true,"middle");
 s.text(95,303,"Retrieved records",13,m,false,"middle");
 for(const [i,r] of rows.entries()){
   s.box(x0,r.y,700,92,C.F[i],C.S[i],C.corner,C.bw,theme==="airy","lane"+r.n);
   s.shape(231,r.y+25,12,C.S[i],theme==="dual"?"square":"circle");
   s.text(231,r.y+25,r.n,13,"#ffffff",true,"middle");
   s.text(250,r.y+25,r.name,18,ink,true);
   small(226,r.y+53,r.methods); if(i===1)s.text(226,r.y+73,"MExGen reuses P1",12,m);
   for(const [j,cell] of r.cells.entries()){
      const x=[410,571,724][j];
      if(theme==="airy")s.box(x-8,r.y+12,[146,143,171][j],67,"#ffffff","#dce6ee",9);
      if(theme==="editorial"){
         const xx=x+4, yy=r.y+71;
         if(j===0){s.box(xx,yy-6,11,14,"#ffffff",C.S[i],2,1.2);s.edge([[xx+3,yy-1],[xx+8,yy-1]],C.S[i],1);s.edge([[xx+3,yy+3],[xx+8,yy+3]],C.S[i],1);}
         if(j===1){s.edge([[xx,yy+4],[xx+4,yy+4],[xx+4,yy-3],[xx+9,yy-3],[xx+9,yy+4],[xx+15,yy+4]],C.S[i],1.3);}
         if(j===2){[6,11,15].forEach((h,k)=>s.box(xx+k*5,yy+5-h,3,h,C.S[i],C.S[i],1));}
      }
      s.text(x,r.y+31,cell[0],15.5,ink,true);
      s.text(x,r.y+55,cell[1],13.1,m);
      if(j<2)line([[x+[145,137][j],r.y+40],[x+[154,146][j],r.y+40]],true,false,C.S[i],1.35);
   }
 }
 s.box(953,184,224,130,theme==="airy"?"#eaf0f5":"#f4f7fa","#8fa4b4",C.corner,C.bw,false,"rank");
 s.box(963,195,204,32,C.dark,"none",8);
 s.text(1065,211,"Attribution ranking",16,"#ffffff",true,"middle");
 s.text(1065,251,"Rank the source scores",15,ink,true,"middle");
 s.text(1065,278,"Keep ties in the top set",14,m,false,"middle");
 s.box(953,332,224,62,"#ffffff","#a3b3c0",9,1,true,"eval");
 line([[1065,314],[1065,331]],true,true,m,1.35,"rank","eval");
 s.text(1065,351,"Offline evaluation",15,ink,true,"middle");
 s.text(1065,376,"Tie-aware gold top-1",14,m,false,"middle");
 s.box(205,411,700,28,"#f5f8fb","#cbd6df",8,1);
 s.text(555,425,"Shared by B and C: one full-context reference a₀. Invalid reference → stop.",14,ink,false,"middle");
 s.box(205,454,972,112,C.route,theme==="dual"?"#6d93bb":"#c8ced8",C.corner,C.bw,theme==="airy");
 s.text(221,470,"Optional cost-aware route",16,ink,true);
 s.box(223,495,206,50,theme==="dual"?"#deedff":"#ffffff","#9fb4c9",9,1,false,"cheap");
 s.text(326,513,"Run LOI or P1",15,ink,true,"middle");
 s.text(326,532,"M + 1 calls incl. a₀",13,m,false,"middle");
 line([[429,520],[461,520]],true,false,m,1.65,"cheap","gate");
 s.shape(508,520,45,"#ffffff","diamond","#8da4b5",1.3,"gate");
 s.text(508,513,"Unique",14,ink,true,"middle");s.text(508,531,"top?",14,ink,true,"middle");
 line([[553,520],[574,520],[574,494],[653,494]],true,false,m,1.65,"gate","return");
 line([[553,520],[574,520],[574,539],[653,539]],true,false,C.S[2],1.8,"gate","escalate");
 s.text(610,484,"yes",12,m,true,"middle");s.text(610,529,"no",12,C.S[2],true,"middle");
 s.box(653,478,178,32,"#ffffff","#b5c3d1",8,1,false,"return");
 s.text(742,494,"Return probe ranking",14,ink,true,"middle");
 s.box(653,523,178,32,theme==="dual"?"#ffe4de":"#ffffff",C.S[2],8,1,false,"escalate");
 s.text(742,539,"Return RM@k ranking",14,ink,true,"middle");
 s.text(851,516,"On escalation, reuse a₀.",14,ink,true);
 s.text(851,539,"At most k further calls.",14,m);
 return s;
}
function plots(D,K){
 const s0=K.ink,m=K.muted,grid="#dbe4eb",line="#8796a2",blue="#1765a2",green="#08765d",orange="#b54e22",black="#283946",gray="#eaf0f4";
 const lab=["HotpotQA","MuSiQue","Qasper","Sym. FEVER"];
 const R=(v,d=2)=>+v.toFixed(d);
 function palette(a,b,t){const p=x=>x.slice(1).match(/.{2}/g).map(v=>parseInt(v,16));const A=p(a),B=p(b);return "#"+A.map((x,i)=>Math.round(x+(B[i]-x)*Math.max(0,Math.min(1,t))).toString(16).padStart(2,"0")).join("");}
 function front(){
  const s=K.scene("Accuracy–cost frontier",1200,712);
  const legend=[["V1",blue,"diamond"],["P1",green,"circle"],["MExGen-LOO",green,"diamond"],["LOI",green,"square"],["RM@k",orange,"circle"],["LOI → RM@k",black,"triangle"]];
  let pos=34;for(const [l,c,k] of legend){s.shape(pos,62,5,k==="triangle"?"#ffffff":c,k,c,1.3);s.text(pos+12,62,l,15,m);pos+=l.length*9+44;}
  const left=156,pw=186,ph=108,cw=205,rh=140,top=117;
  for(const [i,[_,ml]] of D.models.entries())s.text(left+i*cw+pw/2,95,ml,17,s0,true,"middle");
  const fx=v=>R(5+(Math.log10(v)-Math.log10(.85))/(Math.log10(86)-Math.log10(.85))*(pw-10));
  const fy=v=>R(ph-(v-.35)/(.68)*ph);
  for(const [i,o] of D.frontier.entries()){
    const row=Math.floor(i/5),col=i%5,x=left+col*cw,y=top+row*rh;
    s.box(x,y,pw,ph,"#ffffff",grid,4,1);
    for(const p of [.4,.6,.8,1]){const yy=y+fy(p);s.edge([[x,yy],[x+pw,yy]],grid,1);if(col===0)s.text(x-9,yy,p.toFixed(1),13,m,false,"end");}
    for(const v of [1,10,64]){const xx=x+fx(v);s.edge([[xx,y],[xx,y+ph]],grid,1);if(row===3)s.text(xx,y+ph+15,String(v),13,m,false,"middle");}
    if(col===0){s.text(14,y+39,lab[row],14,s0,true);s.text(14,y+59,"Gold top-1",12,m);}
    if(!o.methods.V1){s.text(x+pw/2,y+ph/2,"No results",13,m,false,"middle");continue;}
    const pt=([a,b])=>[R(x+fx(a)),R(y+fy(b))];
    const V=o.methods.V1,vy=pt(V)[1];
    s.edge([[x,vy],[x+pw,vy]],blue,1,true);
    const rm=["RM@8","RM@16","RM@32","RM64"].filter(k=>o.methods[k]).map(k=>pt(o.methods[k]));
    if(rm.length>1)s.edge(rm,orange,2.1);
    rm.forEach(([x,y])=>s.shape(x,y,4,orange,"circle","#ffffff",1));
    if(!rm.length)s.text(x+pw/2,y+ph-26,"RM unavailable",12,m,false,"middle");
    const routes=["LOI->RM@16","LOI->RM@32","LOI->RM64"].map(k=>o.routes.find(v=>v[0]===k)).filter(Boolean).map(v=>pt(v.slice(1)));
    if(routes.length>1)s.edge(routes,black,1.5,true);
    for(const [xx,yy] of routes)s.shape(xx,yy,4.5,"#ffffff","triangle",black,1.2);
    for(const [k,colr,mk] of [["V1",blue,"diamond"],["P1",green,"circle"],["MEXGEN_LOO",green,"diamond"],["LOI",green,"square"]]){
      if(o.methods[k])s.shape(...pt(o.methods[k]),k==="V1"?5.2:4.3,colr,mk,"#ffffff",1.1);
    }
    s.text(x+pw-6,y+ph-9,`n=${o.n}`,12,m,false,"end");
  }
  s.text(668,700,"Nominal calls per instance (log scale)",16,m,false,"middle");
  return s;
 }
 function dist(){
  const s=K.scene("Answer variation and score distributions",1200,424);
  const colsA=["#e2edf8","#9ac0df","#4c91c4","#165483"];
  const colsB=["#d9dee4","#1375ad","#efbd83","#b64c26"];
  const left=[128,522],pw=262;
  s.text(24,69,"(a) Full-context changes",17,s0,true);
  s.text(418,69,"(b) P1 top-set structure",17,s0,true);
  s.text(812,69,"(c) RM64 score percentiles",17,s0,true);
  for(let i=0;i<4;i++){
    const d=D.dist[D.ds[i][0]], y=122+i*53;
    s.text(24,y,lab[i],15,s0,true);
    s.text(418,y,lab[i],15,s0,true);
    s.text(812,y,lab[i],15,s0,true);
    for(const [j,a] of [d.A,d.B].entries()){
      const total=a.reduce((n,v)=>n+v,0),cols=j?colsB:colsA;
      let x=left[j];a.forEach((v,k)=>{
        const w=pw*v/total;if(v)s.box(R(x),y-12,R(w),24,cols[k],"#ffffff",0,.7);
        if(w>=36)s.text(R(x+w/2),y,`${Math.round(100*v/total)}%`,12,k<2&&j===0||j===1&&k%2===0?s0:"#ffffff",true,"middle");
        x+=w;
      }); 
    }
  }
  for(const l of left){
   for(const v of [0,.5,1]){const x=l+pw*v;s.edge([[x,294],[x,304]],line,1);s.text(x,316,`${v*100}%`,13,m,false,"middle");}
   s.edge([[l,299],[l+pw,299]],line,1);s.text(l+pw/2,340,"Share of instances",15,m,false,"middle");
  }
  const labels=[["0 of 3","1 of 3","2 of 3","3 of 3"],["All zero","Unique","2-way","3+ tie"]];
  for(let j=0;j<2;j++)for(let i=0;i<4;i++){const x=[24,418][j]+i*89;s.box(x,369,13,13,[colsA,colsB][j][i],"none",1);s.text(x+18,376,labels[j][i],13,m);}
  const low=916,high=1170,px=v=>R(low+(v+1)/2*(high-low));
  s.edge([[px(0),99],[px(0),296]],line,1,true);
  for(let i=0;i<4;i++){const v=D.dist[D.ds[i][0]];for(const [j,k] of ["gold","nongold"].entries()){
    const a=v[k].quantiles,y=116+i*53+j*13,c=j?"#60798b":blue;
    s.edge([[px(a[0]),y],[px(a[4]),y]],c,1.5);
    s.box(px(a[1]),y-4,Math.max(.8,px(a[3])-px(a[1])),8,c,c,1);
    s.shape(px(a[2]),y,3.5,"#ffffff",j?"square":"diamond",c,1.5);
  }}
  for(const v of [-1,-.5,0,.5,1]){const x=px(v);s.edge([[x,294],[x,304]],line,1);s.text(x,316,String(v),13,m,false,"middle");}
  s.edge([[low,299],[high,299]],line,1);
  s.text((low+high)/2,340,"Banzhaf score",15,m,false,"middle");
  s.shape(832,376,5,blue,"diamond");s.text(843,376,"Gold",13,m);s.shape(904,376,5,"#60798b","square");s.text(916,376,"Non-gold",13,m);
  s.text(812,403,"Median · 25–75% box · 5–95% whiskers",13,m);
  return s;
 }
 function maps(){
  const s=K.scene("Attribution score maps",1200,753);
  
  
  const x0=160,w=218,gap=24,h=244;
  const colors=v=>v<0?palette("#f2f4f5","#b64b26",-v):palette("#f2f4f5","#165e9e",v);
  for(const [j,method] of D.methods.entries())s.text(x0+j*(w+gap)+w/2,92,method,18,s0,true,"middle");
  for(const [i,key] of ["qasper","symfever"].entries()){
    const A=D.mats[key],y0=115+i*289;
    s.text(24,y0+17,lab[i+2],17,s0,true);
    for(let j=0;j<4;j++){
      const x=x0+j*(w+gap),dx=w/10,dy=h/A.length;
      for(let r=0;r<A.length;r++){
        const v=A[r].scores[j];let start=0;
        while(start<10){let end=start+1;if(start!==0)while(end<10&&v[end]===v[start])end++;
          s.box(R(x+start*dx),R(y0+r*dy),R((end-start)*dx),R(dy),colors(v[start]),"none",0,0);start=end;
        }
      }
      s.edge([[x+dx,y0],[x+dx,y0+h]],"#304555",1.5);
      for(let r=1;r<A.length;r++)if(A[r].kind!==A[r-1].kind){const y=R(y0+r*dy);s.edge([[x,y],[x+w,y]],"#ffffff",1.4);}
      s.text(x+dx/2,y0+h+15,"Gold",13,s0,true,"middle");
      s.text(x+dx+(w-dx)/2,y0+h+15,"Other sources",13,m,false,"middle");
    }
    const kinds=["All zero","Unique","2-way tie","3+ tie"];let r=0;
    while(r<A.length){let e=r+1;while(e<A.length&&A[e].kind===A[r].kind)e++;const y=y0+(r+e)*h/(2*A.length);s.text(148,R(y),`${kinds[A[r].kind]} (${e-r})`,12,m,false,"end");r=e;}
  }
  const cX=458,cY=711,bw=23;
  for(let i=0;i<=20;i++)s.box(cX+i*bw,cY,bw,13,colors(i/10-1),"none",0,0);
  for(const [i,l] of [[0,"−1"],[10,"0"],[20,"+1"]])s.text(cX+(i+.5)*bw,737,l,13,m,false,"middle");
  s.text(cX-17,cY+6,"Attribution score",14,m,false,"end");
  return s;
 }
 function heat(){
  const s=K.scene("End-to-end performance heatmap",1200,560);
  s.text(24,26,"End-to-end tie-aware gold top-1",24,s0,true);
  s.text(24,55,"A dash marks an unrun configuration. The four dataset blocks share one scale.",15,m);
  const rows=["V1","V2","V3","V4","V5","V6","V7","P1","P2","P5","MEXGEN_LOO","LOI","RM@16","RM@32","RM64"];
  const left=140,cw=51,rh=27,top=124;
  for(let j=0;j<D.heat.length;j++){
    const u=D.heat[j],x=left+j*cw+Math.floor(j/5)*4;
    if(j%5===0)s.text(x+2.5*cw,82,lab[Math.floor(j/5)],17,s0,true,"middle");
    s.text(x+cw/2,105,u.ml,12.5,m,true,"middle");
    for(let i=0;i<rows.length;i++){
      const k=rows[i],v=u.hm[k],y=top+i*rh;
      const f=v==null?"#f5f7f9":palette("#edf5fb","#175589",(v-.3)/.7);
      s.box(x,y,cw-1,rh-1,f,"#ffffff",0,.7);
      s.text(x+(cw-1)/2,y+(rh-1)/2,v==null?"–":v.toFixed(2),13,v!=null&&v>.78?"#ffffff":m,true,"middle");
      if(j===0)s.text(left-12,y+(rh-1)/2,k==="MEXGEN_LOO"?"MExGen-LOO":k,14,s0,true,"end");
    }
  }
  const xs=842,ys=537;
  for(let i=0;i<10;i++)s.box(xs+i*20,ys,20,10,palette("#edf5fb","#175589",i/9),"none",0,0);
  s.text(xs-9,ys+5,"Gold top-1",12,m,false,"end");
  s.text(xs,ys+17,"0.30",11,m);
  s.text(xs+200,ys+17,"1.00",11,m,false,"end");
  return s;
 }
 return {frontier:front(),dist:dist(),maps:maps(),heatmap:heat()};
}
const K=toolkit(), D=JSON.parse(fs.readFileSync(path.join(__dirname,"figure_inputs.json"),"utf8"));
const OUT=path.join(__dirname,"..","..","gpt");fs.mkdirSync(OUT,{recursive:true});const save=(name,s)=>fs.writeFileSync(path.join(OUT,name),s);
const themes=["editorial","airy","dual"], O=themes.map(t=>overview(t,K));
O.forEach((s,i)=>save("fig_overview_"+themes[i]+".svg",K.svg(s)));
save("fig_overview.drawio",K.drawio(O));
for(const [n,s] of Object.entries(plots(D,K))){
 save("fig_"+n+"_editable.svg",K.svg(s)); save("fig_"+n+"_editable.drawio",K.drawio([s]));
}
