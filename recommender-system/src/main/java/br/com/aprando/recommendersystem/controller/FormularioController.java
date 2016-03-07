package br.com.aprando.recommendersystem.controller;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import javax.servlet.http.HttpServletRequest;

import org.apache.commons.lang3.exception.ExceptionUtils;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import br.com.aprando.recommendersystem.base.ServiceException;
import br.com.aprando.recommendersystem.domain.Avaliacao;
import br.com.aprando.recommendersystem.domain.Produto;
import br.com.aprando.recommendersystem.domain.Questao;
import br.com.aprando.recommendersystem.domain.Usuario;
import br.com.aprando.recommendersystem.service.AvaliacaoService;
import br.com.aprando.recommendersystem.service.ProdutoService;
import br.com.aprando.recommendersystem.service.QuestionarioService;
import br.com.aprando.recommendersystem.service.UsuarioService;

@Controller
@RequestMapping("/formulario")
public class FormularioController {

	@Autowired
	UsuarioService usuarioService;

	@Autowired
	QuestionarioService questionarioService;

	@Autowired
	AvaliacaoService avaliacaoService;
	
	@Autowired
	ProdutoService produtoService;
	

	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String listar(HttpServletRequest request) {
		List<Questao> questoes = new ArrayList<Questao>();
		try {
			questoes.addAll(questionarioService.listarTodos());
			request.setAttribute("questionario", questoes);
		} catch (Exception e) {
			e.printStackTrace();
			request.setAttribute("erro", ExceptionUtils.getStackTrace(e));
			return "erro";
		}
		return "formulario-dissertacao";
	}

	@RequestMapping(value = "/salvar-questionario", method = RequestMethod.POST)
	@ResponseBody
	public String salvarQuestionario(QuestionarioForm formBean) {
		try {
			for (Questao q : formBean.getQuestoes())
				if (q == null || q.getResposta() == null
						|| "".equals(q.getResposta()))
					return "false";

			usuarioService.salvarRespostas(formBean.getIdUsuario(),
					formBean.getQuestoes());
		} catch (Exception e) {
			e.printStackTrace();
			return "false";
		}
		return "true";
	}
	
	@RequestMapping(value = "/carga-questionario", method = RequestMethod.GET)
	@ResponseBody
	public String cargaQuestionario(QuestionarioForm formBean) {
		try {
			Questao q = questionarioService.consultarPorOrdenacao(1);
			if(q == null){
				q = new Questao();
				q.setOrdenacao(1);
			}
			q.setPergunta("Com que frequencia você posta, comenta ou compartilha infos nas redes sociais?");
			q.setAlternativas(Arrays.asList("Durante o dia todo.", "Poucas vezes ao dia.", "Uma vez ao dia.", "Algumas vezes durante a semana.", "Não utilizo redes sociais."));
			questionarioService.salvar(q);
			
			q = questionarioService.consultarPorOrdenacao(2);
			if(q == null){
				q = new Questao();
				q.setOrdenacao(2);
			}
			q.setPergunta("Você sabia que suas informações podem ser utilizadas por empresas para oferecer produtos e serviços especializados?");
			q.setAlternativas(Arrays.asList("Sim, e não me importo!", "Sim, e não gosto disso. Mas uso redes sociais mesmo assim.", "Não sabia, e não me importo!", "Não sabia! Vou parar de utilizar redes sociais."));
			questionarioService.salvar(q);
			
			
		} catch (ServiceException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return "Sucess";
	}	

	@RequestMapping(value = "/salvar-avaliacoes", method = RequestMethod.POST)
	@ResponseBody
	public String salvarAvaliacoes(AvaliacaoForm formBean) {
		try {
			Avaliacao avaliacaoExistente = null;
			
			for (Avaliacao a : formBean.getAvaliacoes()) {
				if (a == null || a.getAvaliacao() == null || "".equals(a.getAvaliacao()))
					continue;
				
				avaliacaoExistente = avaliacaoService.consultarPorIdUsuarioIdProduto(formBean.getIdUsuario(), a.getIdProduto());
				if(avaliacaoExistente != null)
					a.setId(avaliacaoExistente.getId());
				a.setIdUsuario(formBean.getIdUsuario());
				avaliacaoService.salvar(a);

			}
		} catch (Exception e) {
			e.printStackTrace();
			return "false";
		}
		return "true";
	}

	@RequestMapping(value = "/recuperar-recomendacoes", method = RequestMethod.POST)
	@ResponseBody public Produto[] recomendar(Usuario formBean, RedirectAttributes redirectAttrs) {
		List<Produto> produtos = new ArrayList<Produto>();
		Usuario usuario = null;
		try{
			usuario = usuarioService.consultarPorID(formBean.getId());
			if("P".equals(usuario.getStatusRecomendacao()))
				return null;
			
			produtoService.removerProdutosRecomendacao(usuario.getId());
			usuario.setStatusRecomendacao("P");
			usuarioService.salvar(usuario);
			System.out.println("Realizando chamada no spark... UserId:" + formBean.getId());
			
			System.setProperty("user.name", "vagrant"); 
			Runtime rt = Runtime.getRuntime();
//          PRODUCTION
            Process proc = rt.exec( 
					new String[]{ "/home/azureuser/master-thesis-social-recsys/spark-1.4.1-bin-hadoop2.6/bin/spark-submit", "/home/azureuser/master-thesis-social-recsys/machine-learning-module/make_prediction.py", formBean.getId()} );

//          DEVELOPMENT			
// 			Process proc = rt.exec( 
//					new String[]{ "/vagrant/spark-1.6.0-bin-hadoop2.6/bin/spark-submit", "/vagrant/machine-learning-module/make_prediction.py", formBean.getId()} );

			InputStream stderr = proc.getErrorStream();
            InputStreamReader isr = new InputStreamReader(stderr);
            BufferedReader br = new BufferedReader(isr);
            String line = null;
            System.out.println("################ SPARK ###############");
            while ( (line = br.readLine()) != null)
                System.out.println(line);
            System.out.println("################ SPARK ###############");
            int exitVal = proc.waitFor();
            System.out.println("Process exitValue: " + exitVal);
						
			boolean success = false;
			int tentativas = 0; 
			while (tentativas < 20) {
				System.out.println("Tentativa " + tentativas);
				usuario = usuarioService.consultarPorID(formBean.getId());
				if("F".equals(usuario.getStatusRecomendacao())){
					success = true;
					break;
				}
				tentativas++;
				Thread.sleep(5 * 1000);
			}
			
			System.out.println("Todas tentativas realizadas! Sucesso? " + success);
			produtos.addAll(produtoService.buscarProdutosRecomendadosParaUsuario(usuario.getId()));
			
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		} finally {
			try {
				usuario.setStatusRecomendacao("F");
				usuarioService.salvar(usuario);
			} catch (ServiceException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		return produtos.toArray(new Produto[produtos.size()]);
	}	
	

}