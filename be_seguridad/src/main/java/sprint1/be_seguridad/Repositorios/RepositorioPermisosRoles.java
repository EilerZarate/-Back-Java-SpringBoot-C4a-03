package sprint1.be_seguridad.Repositorios;

import org.springframework.data.mongodb.repository.MongoRepository;
import sprint1.be_seguridad.Modelos.PermisosRoles;


public interface RepositorioPermisosRoles extends MongoRepository<PermisosRoles,String> {
}
