package database

import log "github.com/Sirupsen/logrus"

type Season struct {
	sport *Sport
	season string
	path string
}

func (s *Season) ReadSeason() {
	log.WithFields(log.Fields{
		"sport": s.sport.name,
		"season": s.season,
		"path": s.path,
	}).Info("database: reading season")
}
