package br.com.aprando.recommendersystem.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.aprando.recommendersystem.base.ServiceException;
import br.com.aprando.recommendersystem.domain.Produto;
import br.com.aprando.recommendersystem.domain.Questao;


@Transactional
@Service
public class QuestionarioServiceImpl implements QuestionarioService {

	@Autowired
	MongoOperations mongoTemplate;
	
	@Override
	public List<Questao> listarTodos() throws ServiceException {
		Query query = new Query();
		query.with(new Sort(Sort.Direction.ASC, "ordenacao"));
		
		return mongoTemplate.findAll(Questao.class); 
	}

	@Override
	public List<Questao> listarTodosPorIdioma(String idioma) throws ServiceException {
		Query query = new Query();
		query.addCriteria(Criteria.where("idioma").is(idioma));

		return mongoTemplate.find(query, Questao.class);
	}
	
	@Override
	public Questao consultarPorPergunta(String pergunta) throws ServiceException {
		Query query = new Query();
		query.addCriteria(Criteria.where("pergunta").is(pergunta));

		return mongoTemplate.findOne(query, Questao.class);
	}

	@Override
	public Questao salvar(Questao questao) throws ServiceException {
		mongoTemplate.save(questao);
		return questao;
	}	

	@Override
	public Questao consultarPorOrdenacao(Integer ordenacao) throws ServiceException {
		Query query = new Query();
		query.addCriteria(Criteria.where("ordenacao").is(ordenacao));

		return mongoTemplate.findOne(query, Questao.class);
	}
	
}
