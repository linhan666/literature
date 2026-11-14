#!/usr/bin/env python3
"""Create illustrative, explicitly uncited review-plan demo (no reported data)."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root=Path(__file__).resolve().parent
# An original invented image for the optional figure-embedding example.
im=Image.new('RGB',(1280,680),'#FCFDFC'); dr=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
try: f=ImageFont.truetype(font,38); fs=ImageFont.truetype(font,23)
except Exception: f=fs=ImageFont.load_default()
dr.text((60,52),'ILLUSTRATIVE CONCEPT MAP',font=f,fill='#213849')
for i,(x,c,t) in enumerate([(65,'#DDF2EF','Molecular input'),(480,'#E9E4F6','Interaction role'),(894,'#F5E9D6','Evidence test')]):
    dr.rounded_rectangle((x,215,x+314,425),radius=20,fill=c,outline='#B8C6C9',width=3)
    dr.text((x+23,283),t,font=fs,fill='#1B3445')
for x in [383,797]:
    dr.line((x,320,x+89,320),fill='#66788A',width=7)
    dr.polygon([(x+85,308),(x+105,320),(x+85,332)],fill='#66788A')
dr.text((64,576),'DEMO ARTWORK  |  not a reproduced paper figure or empirical result',font=fs,fill='#9E5858')
im.save(root/'demo_concept_art.png')

slides=[
 dict(type='cover', title='显式药物–蛋白 Attention 的综述框架',subtitle='从交互机制、证据类型到条件可比性\nNarrative-Critical Review · 展示用样稿',author='Review Presentation Designer · v1.0',tags=['MAP THE MECHANISMS','TEST THE EVIDENCE','SYNTHESIZE GAPS'],speaker_notes='本样稿只演示综述PPT的叙事与可编辑图示，不是对真实论文进行核验后的结论。'),
 dict(type='big_idea',title='注意力热区 ≠ 已证实的分子互作',section='01  /  核心问题',statement='好看的 Attention Map，\n不等于可信的互作解释。',context='必须区分预测有效、配对依赖、功能归因与结构证据。不同问题需要不同的受控实验。',pillars=['模型能预测什么？','预测是否依赖当前配对？','可视化是否具有物理证据？'],epistemic_status='author_proposed'),
 dict(type='scope',title='先划定“显式跨模态交互”的边界',section='01  /  综述范围',epistemic_status='author_proposed',columns=[
  dict(heading='核心纳入',body='关注由药物与蛋白双方特征共同形成的交互运算。',items=['跨模态 Q/K/V','成对注意力加权','条件化特征重权重']),
  dict(heading='边界案例',body='依据真实公式与代码判断是否产生直接跨模态依赖。',items=['局部与全局作用域','复合注意力模块','论文与代码不一致']),
  dict(heading='不直接等价',body='这些概念不应被自动当作跨模态互作证据。',items=['单模态自注意力','单独的可视化热图','仅在末端拼接特征'])]),
 dict(type='taxonomy',title='以权重的“功能角色”建立操作性分类',section='02  /  方法分类',epistemic_status='author_proposed',parent='显式药物–蛋白交互中的 Attention 权重用途',items=[
  dict(tag='R1',label='Pairwise Joint Pooling',body='以配对权重聚合联合特征'),
  dict(tag='R2',label='Partner-value Transfer',body='跨模态搬运对方的值向量'),
  dict(tag='R3',label='Cross-conditioned Reweighting',body='根据另一模态重标定本模态特征')],takeaway='AUTHOR-PROPOSED：三个角色可重叠，不是互斥的生物结合机制。'),
 dict(type='mechanisms',title='三种候选角色：信息究竟如何跨模态流动？',section='02  /  算子示意',epistemic_status='author_proposed',items=[
  dict(label='ROLE R1',role='联合特征汇聚',input_a='Drug dᵢ',input_b='Protein pⱼ',operator='aᵢⱼ · φ(dᵢ,pⱼ)',output='Pair representation',note='权重作用于联合配对特征'),
  dict(label='ROLE R2',role='跨模态值传递',input_a='Drug Q',input_b='Protein K,V',operator='softmax(QKᵀ) · V',output='Partner-conditioned d',note='值向量来自配对模态'),
  dict(label='ROLE R3',role='条件化特征重权重',input_a='Drug feature',input_b='Protein context',operator='Conditional gate',output='Reweighted features',note='改变本模态的特征强度')]),
 dict(type='lanes',title='P–D–F–S 是四个独立的证据问题',section='03  /  评价框架',epistemic_status='author_proposed',items=[
  dict(code='P',label='Prediction',question='能否预测定义清晰的 DTI 端点？',tests='受控数据划分 · AUROC/AUPRC'),
  dict(code='D',label='Pair Dependence',question='预测是否依赖真实药物–蛋白配对？',tests='受控 partner swap · 单模态对照'),
  dict(code='F',label='Functional Attribution',question='热区是否影响该模型的预测决策？',tests='遮挡 · 干预 · 重要性稳定性'),
  dict(code='S',label='Structural Fidelity',question='关注区域是否吻合可核验的物理互作？',tests='残基接触 · 口袋标注 · 3D基准')]),
 dict(type='comparability',title='先核对五项条件，才能比较论文结论',section='03  /  可比性检查',epistemic_status='author_proposed',checks=['任务与端点：二分类、亲和力或结构接触','数据集与划分：版本、负例、重叠与泄漏','可用信息：序列、分子图、3D、预训练','监督与评价对象：配对、原子、残基、口袋','干预与容量：替换模块、参数量、训练预算'],outcomes=[dict(label='可以比较',body='对所讨论主张的条件已匹配'),dict(label='有条件比较',body='差异已公开，结论明确受限'),dict(label='不宜直接比较',body='关键条件缺失或无法对齐')]),
 dict(type='matrix',title='比较矩阵要呈现“机制与条件”，而非排行榜',section='04  /  方法对照',epistemic_status='author_proposed',columns=['功能角色','跨模态方式','主要输出','可测问题','常见边界'],rows=[
  ['R1 联合汇聚','权重 × pair feature','配对全局表征','P / D / F','未必对应物理接触'],
  ['R2 值传递','Q/K/V 跨来源','条件化 token','P / D / F','信息源需代码核查'],
  ['R3 重权重','另一模态引导门控','重标定特征','P / D / F','不等于显式接触矩阵'],
  ['复合交互','多个操作组合','多层输出','视任务而定','单一角色可能不足'] ],comparison_mode='unmatched',takeaway='示例是机制编码对照，不是经统一基准验证的性能比较。'),
 dict(type='evidence_map',title='文献事实、作者推断与未核实问题必须分开',section='04  /  证据溯源',epistemic_status='author_proposed',items=[
  dict(claim='示例 A：论文原文报告的模型表现',status='source-reported',source='需定位表格/指标'),
  dict(claim='示例 B：综述提出的功能角色分类',status='author-proposed',source='作者框架，待外部检验'),
  dict(claim='示例 C：注意力热区具有物理真实性',status='unresolved',source='需要结构证据'),
  dict(claim='示例 D：不同研究得出相反结论',status='disputed',source='需原文及条件核查')],takeaway='本页仅演示证据编码；所有示例论断均未绑定具体文献。'),
 dict(type='timeline',title='时间演化需要区分三条轨道与有据关系',section='05  /  技术演化',epistemic_status='author_proposed',tracks=[
  dict(label='模型骨架',nodes=[dict(time='概念阶段 A',label='独立模态编码'),dict(time='概念阶段 B',label='显式跨模态交互'),dict(time='概念阶段 C',label='多层组合')]),
  dict(label='方法适配',nodes=[dict(time='概念阶段 A',label='权重聚合'),dict(time='概念阶段 B',label='条件信息传递'),dict(time='概念阶段 C',label='可解释性干预')]),
  dict(label='应用/证据',nodes=[dict(time='概念阶段 A',label='DTI 标签预测'),dict(time='概念阶段 B',label='泛化与泄漏检验'),dict(time='概念阶段 C',label='结构交互核验')])],takeaway='示意轨道无真实年份；横向位置不构成“论文继承关系”的证据。'),
 dict(type='debate',title='为什么“注意力即解释”仍然需要谨慎？',section='05  /  争议与边界',epistemic_status='synthesis_inference',left=dict(heading='可视化提供假设线索',body='权重图能够展示模型内部的聚焦区域，便于提出候选交互解释。',evidence='证据需求：稳定性、功能干预、机制辨识'),right=dict(heading='热区不足以证明物理接触',body='权重可能受特征构造、训练目标与数据偏差影响，未必对应实验结构。',evidence='证据需求：独立结构标签、匹配对照'),resolution='综合判断：先明确解释对象，再用可证伪实验检验。'),
 dict(type='agenda',title='研究空白可转化为三个可执行测试',section='06  /  研究议程',epistemic_status='author_proposed',items=[
  dict(number='01',heading='统一机制对照',method='在固定编码器与训练预算下，逐一替换交互算子。',deliverable='配对条件下的增益归因'),
  dict(number='02',heading='检验配对依赖',method='设计受控 partner-swap 与单模态干预。',deliverable='预测依赖是否真实跨模态'),
  dict(number='03',heading='对齐结构证据',method='在具有口袋/接触标签的数据上，评估空间忠实性。',deliverable='区分解释与物理真实性')]),
 dict(type='figure',title='原始科研图片可以保留，但必须追踪来源',section='06  /  图像溯源',epistemic_status='author_proposed',path='demo_concept_art.png',caption='原创演示图：从输入表征到证据评价的概念流程。',credit='Original demonstration artwork. No external paper image or empirical measurements. Not evidence-verified.'),
 dict(type='synthesis',title='结论必须分层，而不是把所有洞见都称为发现',section='07  /  批判性综合',epistemic_status='author_proposed',items=[
  dict(status='可讨论的事实问题',title='模型预测能力',body='应限定到任务、数据和真实评价协议。'),
  dict(status='作者提出的框架',title='R1 / R2 / R3 编码',body='需要更多真实实现核验与边界检验。'),
  dict(status='待补证据',title='注意力与结构接触',body='仅凭热图无法完成物理层面的证实。'),
  dict(status='后续关键争议',title='跨模型公平比较',body='不同信息与训练条件可改变结论。')]),
 dict(type='closing',title='结论',statement='从“模型名称”比较\n走向“机制 × 证据 × 条件”比较',points=['机制分类应有可操作、可复核的定义。','不同评价问题必须采用相匹配的证据。','先核对条件，再讨论性能差异与研究空白。'])
]
plan=dict(deck_title='药物–蛋白 Attention 综述',subtitle='Review talk demo',author='Review Presentation Designer',mode='demo',language='zh',theme='editorial-light',disclaimer='DEMO — not source verified',slides=slides)
(root/'demo_review_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
for fn,header in [
 ('sources.sample.csv','source_id,title,authors,year,doi_or_url,source_file,identity_status,notes'),
 ('claims.sample.csv','claim_id,claim_text,epistemic_status,verification_status,source_ids,source_locator,verification_basis,comparability_scope,limitations,slide_ids'),
 ('figure_manifest.sample.csv','figure_id,slide_id,file_path,figure_type,source_id,source_page,adapted_or_reproduced,license_or_permission,transformations,notes')]:
 (root/fn).write_text(header+'\n',encoding='utf-8')
print('Generated',len(slides),'slide demo plan and original placeholder artwork')
