"use strict";(self["webpackChunktodo_front"]=self["webpackChunktodo_front"]||[]).push([[387],{3187:function(e,l,a){a.r(l),a.d(l,{default:function(){return K}});a(7658);var t=a(6252),s=a(3577),u=a(9963),n=a(2262),i=a(3392),o=a(3100),d=a(9980),v=a.n(d),c=a(5762),r=a(2791);const k=e=>((0,t.dD)("data-v-0f0fd8d5"),e=e(),(0,t.Cn)(),e),p={class:"grid-container"},_=k((()=>(0,t._)("div",{class:"demo"},[(0,t._)("p",null," This page is for demonstration purposes only. All data will be lost after a page refresh ")],-1))),m={class:"grid-item-todo"},f={key:0,class:"no-tasks",style:{display:"flex","flex-direction":"column"}},h=k((()=>(0,t._)("h2",null,"No Tasks to Display",-1))),g={key:1},w={class:"unselectable"},y={class:"flex-headers"},b=k((()=>(0,t._)("div",{class:"header-number"},"#",-1))),x=k((()=>(0,t._)("div",{class:"header-text"},"Description",-1))),D={class:"header-edit"},S={class:"header-delete"},C=k((()=>(0,t._)("div",{class:"header-completed"},"Status",-1))),H={class:"flexbox"},z={class:"flex-id"},U=["contenteditable","onBlur"],T=["onMouseover"],E=["onClick"],I=["onClick"],M=["onClick","src"],O=["onSubmit"],W=k((()=>(0,t._)("button",{class:"button-74"},"add task",-1))),B={key:2,class:"invalid-input"},F={class:"grid-item-calendar"},V={key:0,class:"task-status"},q={id:"total-tasks"},A={id:"complete-tasks"},P={id:"uncomplete-tasks"};var Z={__name:"TheDemo",setup(e){const l=(0,n.iH)((new Date).toISOString().slice(0,10)),d=(0,n.iH)(!1),k=(0,n.iH)(""),Z=(0,n.iH)(""),N=(0,n.qj)([]),j=(0,n.iH)([]),K=(0,n.iH)(!1);0===N.filter((e=>"2022-11-28"===e["date"])).length?K.value=!1:(j.value=N.filter((e=>"2022-11-28"===e["date"]))[0],K.value=!0);const L=(0,n.iH)(null),Y=(0,n.iH)(null),G=(0,n.iH)(null),J=(0,n.iH)(null);function Q(e){return e.toLocaleDateString("en-US",{month:"long",year:"numeric",day:"numeric"})}j.value.length>0&&(Y.value=j.value.tasks.filter((e=>!e.completed)).length),(0,t.YP)([j],(()=>{"date"in j.value?(J.value=j.value.tasks.length,Y.value=j.value.tasks.filter((e=>!e.completed)).length,G.value=J.value-Y.value):(J.value=null,G.value=null,Y.value=null)}),{deep:!0});const R=e=>{l.value=e.toISOString().slice(0,10),j.value=N.filter((e=>e["date"]===l.value))[0],K.value=!0,j.value||(j.value=(0,n.iH)([]),K.value=!1)};function X(e){Z.value=e.target.innerText}function $(e){j.value.tasks.forEach(((l,a)=>{e.task_id==l.task_id&&(j.value.tasks[a].editable=!j.value.tasks[a].editable)}))}function ee(e){Z.value&&j.value.tasks.forEach(((l,a)=>{e.task_id===l.task_id&&(j.value.tasks[a].text=Z.value)}))}const le=(0,n.iH)([a(6697),a(2160)]);function ae(){""!==k.value?("date"in j.value||(j.value={date:l.value,tasks:[]}),j.value.tasks.push({text:k.value,priority:j.value.tasks.length+1,completed:!1,task_id:(Math.random()+1).toString(36).substring(7)}),k.value="",K.value=!0,N.push(j.value)):d.value=!0}function te(){d.value=!1}function se(e){let l=j.value.tasks.indexOf(e);j.value.tasks.splice(l,1),0===j.value.tasks.length&&(K.value=!1),ne()}function ue(e){let l=j.value.tasks.indexOf(e);j.value.tasks[l].completed=!j.value.tasks[l].completed}function ne(){j.value.tasks.forEach(((e,l)=>{j.value.tasks[l].priority=l+1}))}return(e,a)=>{const Z=(0,t.up)("the-header"),N=(0,t.up)("the-footer");return(0,t.wg)(),(0,t.iD)("div",p,[(0,t.Wm)(Z,{class:"header"}),_,(0,t._)("div",m,[(0,t.Wm)(c.Z,null,{default:(0,t.w5)((()=>[K.value?((0,t.wg)(),(0,t.iD)("div",g,[(0,t._)("h1",w,(0,s.zw)("Invalid Date"!==Q(new Date(j.value.date))?Q(new Date(j.value.date)):""),1),(0,t._)("div",y,[b,x,(0,t.wy)((0,t._)("div",D,"Edit",512),[[u.F8,L.value]]),(0,t.wy)((0,t._)("div",S,"Del.",512),[[u.F8,L.value]]),C])])):((0,t.wg)(),(0,t.iD)("div",f,[(0,t._)("div",null,(0,s.zw)(Q(new Date(l.value))),1),h])),(0,t.Wm)((0,n.SU)(v()),{list:j.value.tasks,"item-key":"task_id",onChange:ne},{item:(0,t.w5)((({element:e})=>[(0,t._)("div",H,[(0,t._)("div",z,[(0,t._)("p",null,(0,s.zw)(e.priority),1)]),(0,t._)("div",{class:(0,s.C_)(["flex-text",{editSelectedBorder:e.editable}])},[(0,t._)("p",{contenteditable:e.editable,onInput:X,onBlur:l=>ee(e)},(0,s.zw)(e.text),41,U)],2),(0,t._)("div",{class:"flex-buttons",onMouseover:l=>L.value=e.priority,onMouseout:a[0]||(a[0]=e=>L.value=null)},[(0,t.wy)((0,t._)("img",{src:i,class:(0,s.C_)(["edit-img",{editSelected:e.editable}]),onClick:l=>$(e)},null,10,E),[[u.F8,L.value===e.priority]]),(0,t.wy)((0,t._)("img",{src:o,alt:"delete-image",class:"delete-img",onClick:l=>se(e)},null,8,I),[[u.F8,L.value===e.priority]]),(0,t._)("img",{onClick:l=>ue(e),src:e.completed?le.value[0]:le.value[1],alt:"status",class:"status-img"},null,8,M)],40,T)])])),_:1},8,["list"]),(0,t._)("div",null,[(0,t._)("form",{class:"form-control",onSubmit:(0,u.iM)(ae,["prevent"])},[(0,t.wy)((0,t._)("input",{class:"task-input",onBlur:te,onKeyup:te,"onUpdate:modelValue":a[1]||(a[1]=e=>k.value=e),type:"text","aria-label":"Add task"},null,544),[[u.nr,k.value]]),W],40,O)]),d.value?((0,t.wg)(),(0,t.iD)("span",B,"Please Enter Text")):(0,t.kq)("",!0)])),_:1})]),(0,t._)("div",F,[(0,t._)("h1",null,(0,s.zw)(l.value),1),(0,t.Wm)((0,n.SU)(r.Z),{inline:"",enableTimePicker:!1,monthChangeOnScroll:!1,modelValue:l.value,"onUpdate:modelValue":[a[2]||(a[2]=e=>l.value=e),R],autoApply:""},null,8,["modelValue"]),J.value?((0,t.wg)(),(0,t.iD)("div",V,[(0,t._)("p",null,[(0,t.Uk)(" # Tasks: "),(0,t._)("span",q,(0,s.zw)(J.value),1)]),(0,t._)("p",null,[(0,t.Uk)(" # Completed tasks: "),(0,t._)("span",A,(0,s.zw)(G.value),1)]),(0,t._)("p",null,[(0,t.Uk)(" # Not completed tasks: "),(0,t._)("span",P,(0,s.zw)(Y.value),1)])])):(0,t.kq)("",!0)]),(0,t.Wm)(N,{class:"footer"})])}}},N=a(3744);const j=(0,N.Z)(Z,[["__scopeId","data-v-0f0fd8d5"]]);var K=j}}]);