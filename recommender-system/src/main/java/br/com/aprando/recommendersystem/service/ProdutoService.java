package br.com.aprando.recommendersystem.service;

import java.util.Collection;
import java.util.List;
import java.util.Set;

import br.com.aprando.recommendersystem.base.ServiceException;
import br.com.aprando.recommendersystem.domain.Produto;

public interface ProdutoService {

	List<Produto> listarTodos() throws ServiceException;

	Produto consultarPorID(String id) throws ServiceException;

	Produto salvar(Produto produto) throws ServiceException;

	void remover(String id) throws ServiceException;

	List<Produto> listarTodos(int pageNumber) throws ServiceException;

	int getTotalPaginas() throws RuntimeException;

	Set<Produto> buscarProdutosRecomendadosParaUsuario(String id);

	List<Produto> buscarProdutosPopulares();
	
	void removerProdutosRecomendacao(String userId);

}
