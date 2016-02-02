package br.com.aprando.recommendersystem.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.data.mongodb.core.query.BasicQuery;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

import br.com.aprando.recommendersystem.base.ServiceException;
import br.com.aprando.recommendersystem.domain.Produto;
import br.com.aprando.recommendersystem.domain.Recomendacao;

import com.restfb.types.User;

@Service
public class ProdutoServiceImpl implements ProdutoService {

	public static final int PAGE_SIZE = 10;

	@Autowired
	MongoOperations mongoTemplate;

	
	@Override
	public List<Produto> listarTodos() throws ServiceException {
		Query q = new Query();
		q.fields().include("id").include("descricaoCurta").include("nome");
		return mongoTemplate.find(q, Produto.class);
	}

	@Override
	public List<Produto> listarTodos(int pageNumber) throws ServiceException {
		Query q = new Query();
		q.with(new PageRequest(pageNumber - 1, PAGE_SIZE));
		return mongoTemplate.find(q, Produto.class);
	}

	@Override
	public Produto consultarPorID(String id) throws ServiceException {
		Query query = new Query();
		query.addCriteria(Criteria.where("id").is(id));

		return mongoTemplate.findOne(query, Produto.class);
	}

	@Override
	public Produto salvar(Produto produto) throws ServiceException {
		mongoTemplate.save(produto);
		return produto;
	}

	@Override
	public void remover(String id) throws ServiceException {
		mongoTemplate.remove(Criteria.where("id").is(id));
	}

	@Override
	public int getTotalPaginas() throws RuntimeException {
		Query q = new Query();
		double totalDocs = mongoTemplate.count(q, Produto.class);

		int totalPaginas = 1;
		if (totalDocs > PAGE_SIZE)
			totalPaginas = (int) Math.round(totalDocs / PAGE_SIZE);

		return totalPaginas;
	}

	@Override
	public List<Produto> buscarProdutosRecomendadosParaUsuario(String id) {
		Query q = new Query();
		q.addCriteria(Criteria.where("userId").is(id));
		List<Recomendacao> recomendacoes = mongoTemplate.find(q, Recomendacao.class);
		List<Produto> produtos = new ArrayList<>();
		if(recomendacoes != null && !recomendacoes.isEmpty()) {
			for(Recomendacao rec : recomendacoes){
				produtos.addAll(rec.getProducts());
			}
		}
		return produtos;
		
	}

	@Override
	public List<Produto> buscarProdutosPopulares() {
//		Query q = new Query();
//		q.fields().include("id").include("descricaoCurta").include("nome");
//		return mongoTemplate.find(q, Produto.class);
		return null;
	}

}