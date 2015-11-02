// JavaScript Document
var dataStatisticals = [
	{% for key,otuStatistical in otuStatisticals %}
		{sampleName:"{{ otuStatistical.sampleName }}",ampliconType:"{{ otuStatistical.amplicon_type }}",cleanReads:"{{ otuStatistical.clean_read }}",Q20:"{{ otuStatistical.q20 }}",Q30:"{{ otuStatistical.q30 }}",singleton:"{{ otuStatistical.singleton }}",singletonRatio:"{{ otuStatistical.singleton_ratio }}",mappedReads:"{{ otuStatistical.mapped_reads }}",mappedRatio:"{{ otuStatistical.mapped_ratio }}",OTUs:"{{ otuStatistical.otus }}"},
	{% endfor %}
	];
jQuery().ready(function (){
	jQuery("#list47").jqGrid({
		data: dataStatisticals,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['Sample name','Amplicon type', 'clean reads','Q20(%)','Q30(%)','singleton','singleton(%)','mapped reads','mapped reads(%)','OTUs'],
		colModel:[
			{name:'sampleName',index:'sampleName',align:"center", width:90},
			{name:'ampliconType',index:'ampliconType', align:"center",width:90},
			{name:'cleanReads',index:'cleanReads', width:90,align:"center",sorttype:"int"},
			{name:'Q20',index:'Q20', width:90, align:"center",sorttype:"float"},		
			{name:'Q30',index:'Q30', width:90,align:"center",sorttype:"float"},
			{name:'singleton',index:'singleton', width:90,align:"center",sortype:"int"},	
			{name:'singletonRatio',index:'singletonRatio', align:"center",width:90, sortype:"float"},	
			{name:'mappedReads',index:'mappedReads', align:"center",width:90, sortype:"int"},
			{name:'mappedRatio',index:'mappedRatioss', align:"center",width:90, sortype:"float"},
			{name:'OTUs',index:'OTUs', width:90,align:"center", sortype:"int"}
		],
		pager: "#plist47",
		viewrecords: true,
		caption: "样品数据和OTU统计"
	});

 })
 


var otuStatisticalDownsizes=[
	
 {% for key,otuStatisticalDownsize in otuStatisticalDownsizes %}
		
 {sampleName:"{{ otuStatisticalDownsize.sample_name }}",downsize:"{{ otuStatisticalDownsize.downsize }}",otus_before:"{{ otuStatisticalDownsize.otus_before }}",otus_after:"{{ otuStatisticalDownsize.otus_after }}"},
	{% endfor %}
];
jQuery().ready(function (){
	jQuery("#list48").jqGrid({
		data: otuStatisticalDownsizes,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['sampleName','downsize', 'otus_before', 'otus_after'],
		colModel:[
			{name:'sampleName',index:'sampleName', width:140,align:"center"},
			{name:'downsize',index:'downsize', width:140, sorttype:"int",align:"center"},
			{name:'otus_before',index:'otus_before', width:140,align:"center", sortype:"int"},
			{name:'otus_after',index:'otus_after', width:140,align:"center", sortype:"int"}	
		],
		pager: "#plist48",
		viewrecords: true,
		caption: "抽平后样品OTU统计"
	});
 })



var coreMicrobiomes=[
	
 {% for key,coreMicrobiome in coreMicrobiomes.items() %}
		
 {otuId:"{{ coreMicrobiome.otu_id }}",taxonomyLevel:"{{ coreMicrobiome.taxonomy_level }}",taxonomyName:"{{ coreMicrobiome.taxonomy_name }}"},
	{% endfor %}	
];
 jQuery().ready(function (){
	jQuery("#list49").jqGrid({
		data: coreMicrobiomes,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['otuName','taxonomyLevel', 'taxonomyName'],
		colModel:[
			{name:'otuId',index:'otuId', width:90,align:"center", sortype:"int"},
			{name:'taxonomyLevel',index:'taxonomyLevel', width:200,align:"center", sortype:"int"},
			{name:'taxonomyName',index:'taxonomyName', width:140,align:"center", sortype:"int"}
		],
		pager: "#plist49",
		viewrecords: true,
		caption: "core microbiome OTU列表"
	});
 })



var otuAssignmentsStatisticals=[
	
	 {% for  key,otuAssignmentsStatistical in otuAssignmentsStatisticals.items() %}
		
	 {otuName:"{{ key }}",num:"{{ otuAssignmentsStatistical.num }}"},
	
	 {% endfor %}	
];
 
	jQuery().ready(function (){
	jQuery("#list50").jqGrid({
		data: otuAssignmentsStatisticals,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['otuName','num'],
		colModel:[
			{name:'otuName',index:'otuName', width:140,align:"center", sortype:"int"},
			{name:'num',index:'num', width:140,align:"center", sortype:"int"}	
		],
		pager: "#plist50",
		viewrecords: true,
		caption: "OTU注释统计"
	});
 })

var alpha_diversitys=[
	
 {% for key,alphaDiversity in alpha_diversitys.items() %}
		
 {sampleName:"{{ alphaDiversity.alphaName }}",chao1:"{{ alphaDiversity.chao1 }}",goodsCoverage:"{{ alphaDiversity.goods_coverage }}",observedSpecies:"{{ alphaDiversity.observed_species }}",wholeTree:"{{ alphaDiversity.whole_tree }}",shannon:"{{ alphaDiversity.shannon }}",simpon:"{{ alphaDiversity.simpon }}"},
	{% endfor %}	
];
 
 jQuery().ready(function (){
	jQuery("#list51").jqGrid({
		data: alpha_diversitys,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['sampleName','chao1', 'goodsCoverage', 'observedSpecies','wholeTree','shannon','simpon'],
		colModel:[
			{name:'sampleName',index:'sampleName', width:90,align:"center", sortype:"int"},
			{name:'chao1',index:'chao1', width:90,align:"center", sortype:"float"},
			{name:'goodsCoverage',index:'goodsCoverage', width:90,align:"center", sortype:"float"},
			{name:'observedSpecies',index:'observedSpecies', width:90,align:"center", sortype:"float"},
			{name:'wholeTree',index:'wholeTree', width:90,align:"center", sortype:"float"},		
			{name:'shannon',index:'shannon', width:90,align:"center", sortype:"float"},		
			{name:'simpon',index:'simpon', width:90,align:"center", sortype:"float"}		
		],
		pager: "#plist51",
		viewrecords: true,
		caption: "样品Alpha多样性统计结果"
	});
 })
{% if alpha_diff_exist %} 
var alpha_diversity_diffs=[

{% for key,alphaDiversity in alpha_diversity_diffs.items() %}
		
{sampleName:"{{ alphaDiversity.alphaName }}",chao1:"{{ alphaDiversity.chao1 }}",goodsCoverage:"{{ alphaDiversity.goods_coverage }}",observedSpecies:"{{ alphaDiversity.observed_species }}",wholeTree:"{{ alphaDiversity.whole_tree }}",shannon:"{{ alphaDiversity.shannon }}",simpon:"{{ alphaDiversity.simpon }}"},
	{% endfor %}	
];
 
 jQuery().ready(function (){
	jQuery("#list52").jqGrid({
		data: alpha_diversity_diffs,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['sampleName','chao1', 'goodsCoverage', 'observedSpecies','wholeTree','shannon','simpon'],
		colModel:[
			{name:'sampleName',index:'sampleName', width:90,align:"center", sortype:"float"},
			{name:'chao1',index:'chao1', width:90,align:"center", sortype:"float"},
			{name:'goodsCoverage',index:'goodsCoverage', width:90,align:"center", sortype:"float"},
			{name:'observedSpecies',index:'observedSpecies', width:90,align:"center", sortype:"float"},
			{name:'wholeTree',index:'wholeTree', width:90,align:"center", sortype:"float"},		
			{name:'shannon',index:'shannon', width:90,align:"center", sortype:"float"},		
			{name:'simpon',index:'simpon', width:90,align:"center", sortype:"float"}		
		],
		pager: "#plist52",
		viewrecords: true,
		caption: "Alpha diversity指数差异检验"
	});
 })
 
{% endif %}


{% if beta_diversity_exist %}
 var beta_diversitys=[
 {% for beta_diversity in beta_diversity_data %}
 {{ beta_diversity }}	
	{% endfor %}	
 ];
 jQuery().ready(function (){
	jQuery("#list53").jqGrid({
		data: beta_diversitys,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['{{ beta_diversity_sampleName }}'],
		colModel:[
			 {% for beta_diversity in beta_diversity_jqGrid %}
			 {{ beta_diversity }}	
				{% endfor %}		
		],
		pager: "#plist53",
		viewrecords: true,
		caption: "样品Beta diversity统计表（weighted_unifrac）"
	});
 })
{% endif %}

{% if beta_un_diversity_exist %}
 var beta_un_diversitys=[
 {% for beta_diversity in beta_un_diversity_data %}
 {{ beta_diversity }}	
	{% endfor %}	
 ];
jQuery().ready(function (){
	jQuery("#list54").jqGrid({
		data: beta_un_diversitys,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['{{ beta_un_diversity_sampleName }}'],
		colModel:[
			 {% for beta_diversity in beta_un_diversity_jqGrid %}
			 {{ beta_diversity }}	
				{% endfor %}		
		],
		pager: "#plist54",
		viewrecords: true,
		caption: "样品Beta diversity统计表（unweighted_unifrac）"
	});
 })
 {% endif %}
 
{% if diff_otu_marker_exist %}
var diff_otu_markers=[
 {% for value in diff_otu_marker_data %}
 {{ value }}	
	{% endfor %}	
 ];  
jQuery().ready(function (){
	jQuery("#list55").jqGrid({
		data: diff_otu_markers,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['{{ diff_otu_marker_sampleName }}'],
		colModel:[
			 {% for value in diff_otu_marker_jqGrid %}
			 {{ value }}	
				{% endfor %}		
		],
		pager: "#plist55",
		viewrecords: true,
		caption: "差异显著OTU列表"
	});
 })
{% endif %}


{% if diff_genus_marker_exist %}
var diff_genus_markers=[
 {% for value in diff_genus_marker_data %}
 {{ value }}	
	{% endfor %}	
 ]; 
 jQuery().ready(function (){
	jQuery("#list56").jqGrid({
		data: diff_genus_markers,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['{{ diff_genus_marker_sampleName }}'],
		colModel:[
			 {% for value in diff_genus_marker_jqGrid %}
			 {{ value }}	
				{% endfor %}		
		],
		pager: "#plist56",
		viewrecords: true,
		caption: "差异显著物种列表"
	});
 })
{% endif %} 

{% if diff_taxall_marker_exist %}
 var diff_taxall_markers=[
 {% for value in diff_genus_marker_data %}
 {{ value }}	
	{% endfor %}	
 ]; 
 jQuery().ready(function (){
	jQuery("#list57").jqGrid({
		data: diff_taxall_markers,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['{{ diff_taxall_marker_sampleName }}'],
		colModel:[
			 {% for value in diff_taxall_marker_jqGrid %}
			 {{ value }}	
				{% endfor %}		
		],
		pager: "#plist57",
		viewrecords: true,
		caption: "所有水平差异显著物种列表"
	});
 })

{% endif %}

{% if diff_phylum_marker_exist %}
 var diff_phylum_markers=[
 {% for value in diff_phylum_marker_data %}
 {{ value }}	
	{% endfor %}	
 ]; 
 jQuery().ready(function (){
	jQuery("#list58").jqGrid({
		data: beta_diversitysj,
		datatype: "local",
		height: 150,
		rowNum: 10,
		rowList: [10,20,30],
		colNames:['{{ diff_phylum_marker_sampleName }}'],
		colModel:[
			 {% for value in diff_phylum_marker_jqGrid %}
			 {{ value }}	
				{% endfor %}			
		],
		pager: "#plist58",
		viewrecords: true,
		caption: "门差异显著物种列表"
	});
 })
{% endif %}
