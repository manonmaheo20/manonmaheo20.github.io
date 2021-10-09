<!DOCTYPE html>
<html lang="fr">
    
    <head>
        
        <title>Se déplacer en bus</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="../css/style2.css">    
        <link rel="stylesheet" href="../css/grille2.css">
    
    </head>
    
    <body>
        
<!-- PARTIE LOGO -->

        <header> 

            <img src="../images/logostar.png" alt="Logo de la STAR" width="100%" height="100%">

        </header>

<!-- PARTIE MENU -->

        <nav>

            <ul>
                
                <li><a href="../index.html">ACCUEIL</a>

                <li><a href="#">METRO</a>

                    <ul>
                        <li><a href="page_metro_carte.html">Etat des stations métroo</a></li>
                    </ul>

                </li>

                <li><a href="#">BUS</a>
        
                    <ul>
                        <li><a href="page_bus_carte.html">Bus en temps réel</a></li>
                        <li><a href="page_bus_formulaire.html">Station la plus proche</a></li>
                    </ul>

                </li>

                
                <li><a href="#">VELO</a>
        
                    <ul>
                        <li><a href="page_velos_carte.html">Vélos en temps réel</a></li>
                        <li><a href="page_velos_pyramide.html">Emplacements disponibles</a></li>
                    </ul>

                </li>


                <li><a href="#">PARKING</a>

                    <ul>
                        <li><a href="page_parking_carte.html">Parking en temps réel</a></li>
                        <li><a href="page_parking_graphique.html">Graphe des parking</a></li>
                    </ul>
                    
                </li>

            </ul>

        </nav>

    <article>
        
<!-- 			BLOC INFORMATIONS -->

<article>
	<h2>Où vous trouvez-vous ?</h2>

        <form action="formulaire.php" method="post">
            <p>
                Latitude : <input type="text" size="10" name="latitude"> <?php echo "\n"; ?>
                Longitude : <input type="text" size="10" name="longitude"> <?php echo "\n"; ?>
                <input type="submit" value="Calculer distance">
            </p>
        </form>

<?php // Création des dicos des latitudes et longitudes
$latitude = array(
    'Saint-Georges' => 48.112385,
    'Les Lices' => 48.112766, 
    'Guéhenno - Fougères' => 48.119809,
    'Cité Judiciaire' => 48.104771,
    'Préfecture' => 48.128453,
    'Champs Manceaux' => 48.091114,
    'République' => 48.110026,
    'Mairie' => 48.111624,
    'Place Hoche' => 48.115074,
    'Fac de Droit' => 48.118172,
    'Chèques Postaux' => 48.108765,
    'Anatole France' => 48.11817,
    'Paul Bert' => 48.110115,
    'Pontchaillou Métro' => 48.121481,
    'Robidou' => 48.109926,
    'Sainte-Thérèse' => 48.094986,
    'Gros-Chêne' => 48.126795,
    'Pont de Strasbourg' => 48.109859,
    'Musée Beaux-Arts' => 48.109601,
    'Laënnec' => 48.106846,
    'Gares - Solférino' => 48.104162, 
    'Oberthur' => 48.11355,
    'Place de Bretagne' => 48.1097,
    'Pont de Châteaudun' => 48.110264,
    'Plaine de Baud' => 48.112461,
    'Beaulieu Chimie' => 48.116458,
    'Beaulieu Restau U' => 48.122048,
    'La Poterie' => 48.087282,
    'La Courrouze' => 48.099043,
    'Armorique' => 48.129277,
    'Hôtel Dieu' => 48.117596,
    'TNB' => 48.107748,
    'Plélo Colombier' => 48.106125,
    'La Criée' => 48.107626,
    'Horizons' => 48.111621,
    'Auberge de Jeunesse' => 48.120876,
    'Metz - Sévigné' => 48.115993,
    'Villejean-Université' => 48.121076,
    'Berger' => 48.116314,
    'Clemenceau' => 48.093292,
    'Turmel' => 48.122147,
    'Sainte-Anne' => 48.11421,
    'Champs Libres' => 48.105537,
    'Charles de Gaulle' => 48.105111,
    'Pont de Nantes' => 48.102015,
    'La Rotonde' => 48.106653, 
    'Voltaire' => 48.10524,
    'Brest - Verdun' => 48.113009,
    'Marbeuf' => 48.111749,
    'Pierre Martin' => 48.10305,
    'Cucillé' => 48.128788,
    'Jacques Cartier' => 48.097533,
    'Binquenais' => 48.091594,
    'Painlevé' => 48.122994,
    'Gare Sud' => 48.102055,
);

$longitude = array(
    'Saint-Georges' => -1.674417, 
    'Les Lices' => -1.685037, 
    'Guéhenno - Fougères' => -1.66635, 
    'Cité Judiciaire' => -1.68411, 
    'Préfecture' => -1.694032, 
    'Champs Manceaux' => -1.682284, 
    'République' => -1.678037,
    'Mairie' => -1.678757, 
    'Place Hoche' => -1.677073, 
    'Fac de Droit' => -1.670735, 
    'Chèques Postaux' => -1.693432, 
    'Anatole France' => -1.688466, 
    'Paul Bert' => -1.670039, 
    'Pontchaillou Métro' => -1.692737, 
    'Robidou' => -1.659499, 
    'Sainte-Thérèse' => -1.663731, 
    'Gros-Chêne' => -1.665101, 
    'Pont de Strasbourg' => -1.656028, 
    'Musée Beaux-Arts' => -1.67408, 
    'Laënnec' => -1.665814, 
    'Gares - Solférino' => -1.671005, 
    'Oberthur' => -1.661853, 
    'Place de Bretagne' => -1.684041,
    'Pont de Châteaudun' => -1.664443, 
    'Plaine de Baud' => -1.643674, 
    'Beaulieu Chimie' => -1.633875, 
    'Beaulieu Restau U' => -1.638368, 
    'La Poterie' => -1.644121, 
    'La Courrouze' => -1.694512, 
    'Armorique' => -1.675501, 
    'Hôtel Dieu' => -1.677849, 
    'TNB' => -1.673711, 
    'Plélo Colombier' => -1.680482, 
    'La Criée' => -1.680085, 
    'Horizons' => -1.689318, 
    'Auberge de Jeunesse' => -1.681876, 
    'Metz - Sévigné' => -1.658258, 
    'Villejean-Université' => -1.704122, 
    'Berger' => -1.705097, 
    'Clemenceau' => -1.674116, 
    'Turmel' => -1.650808, 
    'Sainte-Anne' => -1.680461, 
    'Champs Libres' => -1.674328,
    'Charles de Gaulle' => -1.677119, 
    'Pont de Nantes' => -1.684015, 
    'La Rotonde' => -1.68677, 
    'Voltaire' => -1.698107, 
    'Brest - Verdun' => -1.693264, 
    'Marbeuf' => -1.702077, 
    'Pierre Martin' => -1.66209, 
    'Cucillé' => -1.698129, 
    'Jacques Cartier' => -1.674307, 
    'Binquenais' => -1.667321, 
    'Painlevé' => -1.660547, 
    'Gare Sud' => -1.673959,
);
/*---------------------------------------------------------------*/
    //  Fonction qui permet de renvoyer 
    function get_distance_m($lat1, $lng1, $lat2, $lng2) {
      $earth_radius = 6378137;   // Terre = sphère de 6378km de rayon
      $rlo1 = deg2rad($lng1);
      $rla1 = deg2rad($lat1);
      $rlo2 = deg2rad($lng2);
      $rla2 = deg2rad($lat2);
      $dlo = ($rlo2 - $rlo1) / 2;
      $dla = ($rla2 - $rla1) / 2;
      $a = (sin($dla) * sin($dla)) + cos($rla1) * cos($rla2) * (sin($dlo) * sin($dlo));
      $d = 2 * atan2(sqrt($a), sqrt(1 - $a));
      return ($earth_radius * $d);
    }
	
   if (isset($_POST["longitude"]) && isset($_POST["latitude"])){
	   //Simplification des notations
        $lat = $_POST['latitude'];
        $longi = $_POST['longitude'];
		
		#On initiale nos variables de comparaison
        $distance_min = 100000000; #Nombre aberrant qui ne peut être atteint
        $nom_proche = ""; #Chaine de caractères vide
        foreach($latitude as $nom => $lati_dico){;
            $distance = get_distance_m(floatval($lat), floatval($longi), floatval($lati_dico), floatval($longitude[$nom]));
			// Si la distance est minimale à celle qui a été stockée précédemment alors on stocke cette nouvelle valeu et on modifie le nom
            if ($distance_min > $distance){
                $distance_min = round($distance, 2);
                $nom_proche = $nom;
            } 
        }
	// Affichage du nom de la station et de la station sous forme de balise html pour l'affiche de la page web
	echo "<h2> Station la plus proche de votre position </h2>";
    echo "<p>La station la plus proche est $nom_proche, elle se trouve à $distance_min mètres</p>";
    }
?>

</article>
    </body>
</html>
