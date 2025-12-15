from flask import Blueprint, jsonify, request
from database import db, DatabaseError

dj_bp = Blueprint('dj', __name__)

@dj_bp.route('/', methods=['GET'])
def get_all_djs():
    try:
        cursor = db.connection.cursor()
        
        cursor.execute("""
            SELECT id, dj_name
            FROM dj
            ORDER BY id
        """)
        
        djs = cursor.fetchall()
        
        if djs:
            result = []
            for dj in djs:
                result.append({
                    'id': dj['id'],
                    'name': dj['dj_name'],
                    'genres': 'Various',  # Default since we don't have genres in DB
                    'image': f'assets/img/dj{dj["id"]}.png',  # Default image pattern
                    'bio': f'KMNR DJ {dj["dj_name"]} brings great music to the airwaves.'
                })
            
            cursor.close()
            return jsonify(result)
        else:
            cursor.close()
            return jsonify([])
            
    except DatabaseError as e:
        print(f"Database error: {e}")
        return jsonify([])
    except Exception as e:
        print(f"Error fetching DJs: {e}")
        return jsonify([])

@dj_bp.route('/<int:dj_id>', methods=['GET'])
def get_dj(dj_id):
    try:
        cursor = db.connection.cursor()
        
        cursor.execute("""
            SELECT id, dj_name
            FROM dj
            WHERE id = %s
        """, (dj_id,))
        
        dj = cursor.fetchone()
        
        if dj:
            result = {
                'id': dj['id'],
                'name': dj['dj_name'],
                'genres': 'Various',
                'image': f'assets/img/dj{dj["id"]}.png',
                'bio': f'KMNR DJ {dj["dj_name"]} brings great music to the airwaves.'
            }
            
            cursor.close()
            return jsonify(result)
        else:
            cursor.close()
            return jsonify({'error': 'DJ not found'}), 404
            
    except DatabaseError as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        print(f"Error fetching DJ: {e}")
        return jsonify({'error': 'Internal error'}), 500