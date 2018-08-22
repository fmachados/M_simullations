#' Simulation of species accessible areas (M in BAM)
#'
#' @description kuenm_m generates an area that has been potentially accessible for a given 
#' species during relevant periods of time.
#'
#' @param occ (character) name of the csv file with all the occurrences used to run the simulation; 
#' columns must be: species, longitude, latitude. 
#' @param vars.folder (character) name of the folder where the environmental variables are. Variables
#' must be in ascii format.
#' @param disp.function (character) dispersal kernel (dispersal function) used to simulate the movement
#' of the species. Options are: "normal", "power_low". Default = "normal".
#' @param function.spread (numeric) Spread of the function ***. Default = 2.
#' @param n.dispersors (numeric) maximum number of dispersors that depart from each colonized pixel. Depending
#' on suitability this number will decrease in less suitable areas.
#' @param suit.threshold (numeric) percentage, . Default = 5.
#' @param n.rep (numeric) number of times that the simulation will be repeated.
#' @param access.threshold (numeric) percentage, . Default = 95.
#' @param out.dir (character) name of the output directory to be created in which subdirectories
#' (according to the \code{ext.type}) containing results of the hierarchical partitioning of the variance 
#' of models will be written. Default = "Hierarchical_partitioning".
#' @param mask.vars (logical) whether or not to mask the variables to the simulated accessible area (M).
#' @param out.varmasked (character) name of the folder to be created to save the masked variables.
#' 
#' @return Folder \code{out.dir} conatining the results of the simulation. These results include: 
#'. A plot of the M and the 
#' occurrences on an environmental layer map will return to the plot window. If \code{mask.vars} = TRUE,
#' the environmental variables will be masked to the M and written in the \code{out.varmasked} folder.
#'
#' @details If any of the potential sources of variation is equal to one (e.g., only one parameter, or 
#' only one climate model), this source of variation will not be considered.

# project = FALSE, steps = 100, for future

kuenm_m <- function(occ, vars.folder, disp.function = "normal", function.spread = 2, 
                    n.dispersors = 4, suit.threshold = 5, n.rep = 100, 
                    access.threshold = 5, out.dir = "M", mask.vars = FALSE, 
                    out.varmasked = "M_variables") {
  
  # install the package if needed
  if(!require(reticulate)){
    install.packages("reticulate")
  }
  
  # testing for initial requirements
  
  reticulate::py_available() # cuando veas algo asi name::name es para usar una funcion de un paquete sin llamarlo
  
  
  use_python("C:/Users/Marlon/AppData/Local/Programs/Python/Python36")
  
  # python simulation
  reticulate::repl_python()
  
  #ALL PYHON CODE
  
  exit
  
  # preparing and writing outputs
  
  
}