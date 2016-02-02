package br.com.aprando.recommendersystem.service;

import java.util.List;

import br.com.aprando.recommendersystem.base.ServiceException;
import br.com.aprando.recommendersystem.domain.Questao;


public interface QuestionarioService {

	List<Questao> listarTodos() throws ServiceException;
	
	List<Questao> listarTodosPorIdioma(String idioma) throws ServiceException;
	
	Questao consultarPorPergunta(String pergunta) throws ServiceException;
	
	Questao consultarPorOrdenacao(Integer ordenacao) throws ServiceException;
	
	Questao salvar(Questao questao) throws ServiceException;
}
